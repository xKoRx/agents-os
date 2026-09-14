"""Executable transcription of the AGENTS OS bootstrap decision rules (Test Model V1).

This module is the ONLY piece of the harness that replicates agent decision
logic. It is a faithful, deterministic transcription of the authorities below;
every rule cites its authority in a comment. It reads real vault files and
never mutates anything.

Authorities transcribed here:
- 80-agents/skills/agents-os-bootstrap/SKILL.md (cold start pasos 1-10,
  warm turn pasos 1-4, entity swap pasos 1-4, Session Modes, Lazy Skill
  Routing, Hard Rules, Output).
- 80-agents/skills/agents-os-context-retrieval/SKILL.md (paso 5, Procedure 2-5,
  Hard Rules) — cited at the retrieval filter.
- 30-resources/agents/skills/meli-agent-dev/SKILL.md y
  30-resources/agents/skills/aranea-agent-dev/SKILL.md (Minimal Reads,
  Procedure 1/3, Hard Rules) — cited at the router packs.
- Ambiguities declared in 80-agents/tools/conformance-harness/artifacts/
  (contract-audit C01-C17, domain-isolation-audit Hallazgos 1-17) are encoded
  as explicit WARN data, never resolved here.

Python 3.9+ stdlib only. Read-only.
"""
from __future__ import annotations

import os
import re
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Canonical paths (bootstrap cold start pasos 1-3; spec fixtures section 4).
# All paths are VAULT_ROOT-relative (constitucion regla 11).
# ---------------------------------------------------------------------------
CONSTITUTION = "80-agents/agents-os/agent-constitution.md"  # bootstrap paso 1
USER_PREF_DIR = "80-agents/memory/public/user-preference/"  # bootstrap paso 1 (resolve by directory)
GLOBAL_INTERNAL = (  # bootstrap paso 2: fixed path, no folder scan
    "80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md"
)
CONTINUITY_ARCHIVE = (  # fixture C14: superseded twin sharing the continuity_key
    "80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity-archive.md"
)
SKILLS_INDEX = "80-agents/skills/INDEX.md"  # bootstrap paso 3
AGENTS_OS_MAP = "80-agents/agents-os/agents-os.md"  # bootstrap paso 4: only if conceptual map needed
FEDERATED_DOMAIN_INDEX = "30-resources/agents/00-index.md"  # bootstrap paso 3: not read without routing need
DOMAIN_ROUTER_REGISTRY = "30-resources/agents/domain-router-registry.md"  # bootstrap paso 6: optional federated config
AGENTS_OS_PROJECT = "10-projects/Personal/AGENTS OS/AGENTS OS.md"  # Hard Rule: not loaded unless maintaining the system

# Domain configuration is federated. The core bootstrap names only this
# optional registry; domains, areas, routers and evidence markers live in its
# rows. The harness parses the same source instead of transcribing the mapping.
REGISTRY_HEADER = ("domain", "areas", "router", "evidence markers")


def parse_domain_registry(text: str) -> List[Dict[str, object]]:
    """Parse the exact four-column Markdown registry contract."""
    routes: List[Dict[str, object]] = []
    for raw in text.splitlines():
        if not raw.startswith("|"):
            continue
        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
        if len(cells) != 4:
            continue
        lowered = tuple(cell.lower() for cell in cells)
        if lowered == REGISTRY_HEADER or all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        domain = cells[0].strip("`").strip().lower()
        areas = [value.strip().lower() for value in re.findall(r"\[\[([^\]]+)\]\]", cells[1])]
        router_match = re.search(r"`([^`]+/SKILL\.md)`", cells[2])
        markers = [value.strip().lower() for value in re.findall(r"`([^`]+)`", cells[3])]
        if not domain or not areas or router_match is None:
            continue
        routes.append({
            "domain": domain,
            "areas": areas,
            "router": router_match.group(1),
            "evidence_markers": markers,
        })
    return routes


def _vault_root_from_here() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def _load_domain_routes() -> List[Dict[str, object]]:
    path = os.path.join(_vault_root_from_here(), DOMAIN_ROUTER_REGISTRY)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return parse_domain_registry(handle.read())
    except OSError:
        return []


DOMAIN_ROUTES = _load_domain_routes()
ROUTERS = {str(route["domain"]): str(route["router"]) for route in DOMAIN_ROUTES}


def _router_preferences(router: str) -> List[str]:
    """Read scoped preferences declared by the router's own Minimal Read."""
    path = os.path.join(_vault_root_from_here(), router)
    try:
        text = open(path, "r", encoding="utf-8").read()
    except OSError:
        return []
    seen: List[str] = []
    for rel in re.findall(r"(?:\.\./)+80-agents/memory/public/user-preference/([a-zA-Z0-9._-]+\.md)", text):
        canonical = "80-agents/memory/public/user-preference/" + rel
        if canonical not in seen:
            seen.append(canonical)
    return seen


ROUTER_PREFS = {domain: _router_preferences(router) for domain, router in ROUTERS.items()}
ARANEA_MCPS_EXPERT = "30-resources/agents/skills/aranea-mcps-expert/SKILL.md"  # C13: sole MCP gate, aranea-only
MELI_SCOPED_PREFS = set(ROUTER_PREFS.get("meli", []))
ARANEA_SCOPED_PREFS = set(ROUTER_PREFS.get("aranea", []))
DOMAIN_GATED_SKILLS = {  # C12/C13: reachable only through their router, never directly
    "meli": {"signals-code-review", "signals-func-spec-authoring", "signals-tech-spec-authoring", "fury-lib-consumer-deploy"},
    "aranea": {"aranea-mcps-expert"},
}

# Meli router Procedure 3 routing table (transcribed subset needed by the
# scenarios; the authoritative table lives in the router SKILL.md itself).
MELI_ROUTER_TABLE = {
    "code_review": "signals-code-review",
}

Entity = Dict[str, object]  # {"title", "path", "area", "slug", "aliases"}


def normalize_area(area: Optional[str]) -> Optional[str]:
    """Strip wiki-link syntax from an area value: '"[[Meli]]"' -> 'meli'."""
    if not area:
        return None
    return area.strip().strip("\"'").strip("[[]]").strip().lower() or None


def domain_from_area(area: Optional[str]) -> Optional[str]:
    """Return one registry domain; zero or ambiguous matches fail closed."""
    key = normalize_area(area)
    if key is None:
        return None
    matches = sorted({str(route["domain"]) for route in DOMAIN_ROUTES if key in route["areas"]})
    return matches[0] if len(matches) == 1 else None


def domains_from_evidence(evidence: Optional[str]) -> List[str]:
    """Resolve explicit task evidence against registry IDs and markers."""
    if not evidence:
        return []
    value = evidence.strip().lower()
    matches: List[str] = []
    for route in DOMAIN_ROUTES:
        domain = str(route["domain"])
        markers = [str(marker) for marker in route["evidence_markers"]]
        if value == domain or any(marker and marker in value for marker in markers):
            matches.append(domain)
    return sorted(set(matches))


class Vault:
    """Read-only view of the real vault used as fixture."""

    def __init__(self, root: str, fm_parser):
        self.root = root
        self._fm = fm_parser  # minimal frontmatter parser injected by the entrypoint

    def abspath(self, rel: str) -> str:
        return os.path.join(self.root, rel)

    def exists(self, rel: str) -> bool:
        return os.path.isfile(self.abspath(rel))

    def read(self, rel: str) -> Optional[str]:
        path = self.abspath(rel)
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()

    def frontmatter(self, rel: str) -> Dict[str, object]:
        text = self.read(rel)
        if text is None:
            return {}
        return self._fm(text)

    def resolve_profile_note(self) -> Optional[str]:
        """Bootstrap paso 1: the single always-load note under user-preference/,
        resolved by that directory (doctor Check 3: exactly ONE; zero means the
        install is incomplete). Returns None when not exactly one."""
        hits: List[str] = []
        pref_dir = self.abspath(USER_PREF_DIR)
        if os.path.isdir(pref_dir):
            for name in sorted(os.listdir(pref_dir)):
                if not name.endswith(".md"):
                    continue
                rel = USER_PREF_DIR + name
                fm = self.frontmatter(rel)
                if str(fm.get("load_policy", "")).strip().strip("\"'") == "always":
                    hits.append(rel)
        return hits[0] if len(hits) == 1 else None

    def resolve_entity(self, title: str) -> Optional[Entity]:
        """Bootstrap paso 5: resolve a user-named entity/slug to the canonical
        Obsidian title by vault search of the note (never by folder scanning of
        skills/memory). Entity homes: Sistema 2 trees (10-projects, 20-areas,
        30-resources/applications). Aliases and slug resolve before the gate
        (paso 5: "Resolve aliases/slugs to the canonical Obsidian title")."""
        want = title.strip().strip("[[]]").strip()
        if not want:
            return None
        trees = ["10-projects", "20-areas", "30-resources/applications"]
        # 1) canonical filename match.
        for tree in trees:
            base = self.abspath(tree)
            for dirpath, dirnames, filenames in os.walk(base):
                dirnames[:] = [d for d in sorted(dirnames) if not d.startswith(".")]
                for fn in sorted(filenames):
                    if fn == want + ".md":
                        rel = os.path.relpath(os.path.join(dirpath, fn), self.root)
                        return self._entity_from_note(rel.replace(os.sep, "/"), want)
        # 2) alias / slug match in frontmatter.
        for tree in trees:
            base = self.abspath(tree)
            for dirpath, dirnames, filenames in os.walk(base):
                dirnames[:] = [d for d in sorted(dirnames) if not d.startswith(".")]
                for fn in sorted(filenames):
                    if not fn.endswith(".md"):
                        continue
                    rel = os.path.relpath(os.path.join(dirpath, fn), self.root).replace(os.sep, "/")
                    fm = self.frontmatter(rel)
                    aliases = fm.get("aliases") or []
                    slug = str(fm.get("slug", "")).strip().strip("\"'")
                    if want.lower() in [str(a).lower() for a in aliases] or (
                        slug and slug.lower() == want.lower()
                    ):
                        return self._entity_from_note(rel, want)
        return None

    def _entity_from_note(self, rel: str, asked: str) -> Entity:
        fm = self.frontmatter(rel)
        title = os.path.splitext(os.path.basename(rel))[0]
        aliases = [str(a) for a in (fm.get("aliases") or [])]
        return {
            "title": title,
            "asked": asked,
            "path": rel,
            "area": fm.get("area"),
            "slug": str(fm.get("slug", "")).strip().strip("\"'"),
            "aliases": aliases,
        }


def domain_gate(
    entity: Optional[Entity],
    surface_evidence: Optional[str] = None,
    task_evidence: Optional[str] = None,
) -> Tuple[Optional[str], str]:
    """Bootstrap step 6: optional registry, zero/one/many fail-closed."""
    evidence_domains = sorted(set(domains_from_evidence(task_evidence) + domains_from_evidence(surface_evidence)))
    if entity is not None:
        area_key = normalize_area(entity.get("area"))
        area_matches = sorted({str(route["domain"]) for route in DOMAIN_ROUTES if area_key in route["areas"]})
        if len(area_matches) > 1:
            return None, "fail-closed: entity area matches multiple registry rows: %s" % ", ".join(area_matches)
        area_domain = area_matches[0] if len(area_matches) == 1 else None
        if len(evidence_domains) > 1 or (evidence_domains and area_domain and evidence_domains != [area_domain]):
            return None, "fail-closed: entity area and task evidence are ambiguous or conflicting"
        if area_domain:
            return area_domain, "entity %s has area %s -> %s (domain router registry)" % (
                entity.get("title"), entity.get("area"), area_domain)
        return None, "area %s has zero registry matches -> no domain router" % (entity.get("area"),)
    if len(evidence_domains) == 1:
        return evidence_domains[0], "no entity resolved; task evidence matched one registry row"
    if len(evidence_domains) > 1:
        return None, "fail-closed: task evidence matched multiple registry rows"
    return None, "no resolvable entity and zero registry matches -> no domain router"


class OpenEvent(object):
    def __init__(self, turn: int, rel: str, reason: str):
        self.turn = turn
        self.rel = rel
        self.reason = reason

    def __repr__(self):
        return "t%d %s (%s)" % (self.turn, self.rel, self.reason)


BASE_STACK_FILES = {CONSTITUTION, GLOBAL_INTERNAL, SKILLS_INDEX}  # + resolved profile


class Session(object):
    """Session state model per bootstrap Session Modes: pick exactly one per
    turn; states session_mode / active_entity / active_domain; warm reuses the
    stack, swap replaces the domain pack explicitly (Session Modes; entity swap
    pasos 1-4: "Never hold two domain packs at once").

    Turn convention: the CALLER fixes `self.turn` to the turn being executed
    before invoking cold_start/warm_turn/swap_entity; the model attributes
    every file open to the current turn and never advances it, so
    opens_in_turn(N) always describes exactly the turn the caller declared
    (adversarial-verification D1: the previous model advanced the turn inside
    warm_turn/swap_entity, which made the scenarios' per-turn assertions
    inspect an always-empty turn)."""

    def __init__(self, vault: Vault):
        self.vault = vault
        self.turn = 0
        self.session_mode = "cold"
        self.active_entity: Optional[Entity] = None
        self.active_domain: Optional[str] = None
        self.base_files: List[str] = []
        self.pack_files: List[str] = []  # domain pack: router + scoped preferences
        self.specialist_skills: List[str] = []
        self.opens: List[OpenEvent] = []
        self.bootstrap_runs = 0
        self.profile_note: Optional[str] = None
        self.gate_note: Optional[str] = None
        self.swap_note: Optional[str] = None
        self._specialist_loaded = False
        self._registry_loaded = False

    # -- file-open telemetry (C06/C07 observable: file-opens per turn) -------
    def open(self, rel: str, reason: str) -> Optional[str]:
        if not self.vault.exists(rel):
            return rel  # missing fixture: recorded as an unresolvable open
        self.opens.append(OpenEvent(self.turn, rel, reason))
        return None

    def opens_in_turn(self, turn: int) -> List[str]:
        return [e.rel for e in self.opens if e.turn == turn]

    def all_opens(self) -> List[str]:
        return [e.rel for e in self.opens]

    # -- cold start (bootstrap pasos 1-10) -----------------------------------
    def cold_start(self, request: dict) -> List[str]:
        """Replicate the cold start decisions and record every file open.

        request keys: entity_title (Optional[str]), casual (bool),
        intent (Optional[str]), surface_evidence/task_evidence (Optional[str]),
        specialist_task (Optional[str]).
        """
        self.bootstrap_runs += 1  # Hard Rules: this skill is the only startup; once per session
        missing: List[str] = []
        # paso 1: constitution + the single always note under user-preference
        # (resolved by directory, not by filename).
        missing += [x for x in [self.open(CONSTITUTION, "paso 1 constitucion")] if x]
        self.profile_note = self.vault.resolve_profile_note()
        if self.profile_note is None:
            raise RuntimeError("cold set broken: no unique always-load note under %s (bootstrap paso 1, doctor Check 3)" % USER_PREF_DIR)
        missing += [x for x in [self.open(self.profile_note, "paso 1 perfil global (unica always de user-preference)")] if x]
        # paso 2: exactly ONE global internal note, fixed path, no folder scan.
        missing += [x for x in [self.open(GLOBAL_INTERNAL, "paso 2 nota interna global (ruta fija)")] if x]
        # paso 3: skills registry; the federated domain index is NOT read
        # without a routing need.
        missing += [x for x in [self.open(SKILLS_INDEX, "paso 3 registro de skills")] if x]
        # paso 4: agents-os.md only if the task needs the conceptual map — the
        # scenarios never do, so it is not opened (no ritual).
        self.base_files = [CONSTITUTION, self.profile_note, GLOBAL_INTERNAL, SKILLS_INDEX]
        # paso 5: identify/resolve the active entity from the request.
        title = request.get("entity_title")
        entity = self.vault.resolve_entity(title) if title else None
        self.active_entity = entity
        # paso 6: optional federated registry, read only when routing has an
        # entity or explicit task evidence to evaluate.
        if entity is not None or request.get("surface_evidence") or request.get("task_evidence"):
            self._ensure_registry()
        domain, note = domain_gate(
            entity,
            surface_evidence=request.get("surface_evidence"),
            task_evidence=request.get("task_evidence"),
        )
        self.gate_note = note
        self.active_domain = domain
        if domain:
            self._load_domain_pack(domain)
        # paso 7: entity retrieval only if the request needs vault state; casual
        # requests skip it (this harness does not open memory for casual turns).
        # paso 9: at most ONE additional specialized skill, only via the router
        # table when a domain router is active (Lazy Skill Routing).
        if request.get("specialist_task") and domain:
            self.route_specialist(domain, request["specialist_task"])
        self.session_mode = "cold"
        return missing

    def _ensure_registry(self) -> None:
        if self._registry_loaded:
            return
        self.open(DOMAIN_ROUTER_REGISTRY, "paso 6 registro federado de routers")
        self._registry_loaded = True

    def _load_domain_pack(self, domain: str) -> None:
        """Minimal reads of the router: the router SKILL.md + the scoped
        preferences it owns (meli-agent-dev / aranea-agent-dev Minimal Reads;
        bootstrap paso 6)."""
        if self.active_domain == domain and self.pack_files:
            return
        self.pack_files = []
        self._open_pack_file(ROUTERS[domain], "paso 6 router de dominio")
        for pref in ROUTER_PREFS[domain]:
            self._open_pack_file(pref, "paso 6 preferencia scoped del router")
        self.active_domain = domain

    def _open_pack_file(self, rel: str, reason: str) -> None:
        miss = self.open(rel, reason)
        if miss is None:
            self.pack_files.append(rel)

    def route_specialist(self, domain: str, task: str) -> Optional[str]:
        """Bootstrap paso 9 + router Procedure 3: at most ONE specialized skill,
        selected through the router's routing table (domain-gated skills route
        through their domain router, never directly from INDEX)."""
        if self._specialist_loaded:
            return None
        if domain == "meli" and task in MELI_ROUTER_TABLE:
            skill = MELI_ROUTER_TABLE[task]
            rel = "30-resources/agents/skills/%s/SKILL.md" % skill
            miss = self.open(rel, "paso 9 skill especializada via tabla del router meli-agent-dev")
            if miss is None:
                self.specialist_skills.append(rel)
                self._specialist_loaded = True
                return rel
        return None

    # -- warm turn (bootstrap warm pasos 1-4) ---------------------------------
    def warm_turn(self, request: dict) -> List[str]:
        """Reuse the stack; fetch only the delta; never re-read
        constitution/profile/bootstrap (Session Modes: "Warm turn, same entity
        ... Never re-read constitution/profile/bootstrap"; warm paso 4: "Do not
        invoke or reread bootstrap merely because the user sent another
        message"). The delta is retrieved lazily by the caller via retrieve()
        and open_delta().

        The return value is the REAL telemetry of this call — the file opens
        recorded during it (zero in the faithful transcription), not a
        constant: a warm turn that re-read a base file would be visible both
        here and in opens_in_turn() of the calling scenario (adversarial-
        verification D1)."""
        before = len(self.opens)
        self.session_mode = "warm"
        return [e.rel for e in self.opens[before:]]

    def retrieve(self, intent: str, explicit_history: bool = False) -> List[str]:
        """Lazy retrieval over the real memory corpus (agents-os-context-
        retrieval paso 5 and Procedure 2-5):

        - "Bootstrap already loaded the base invariants on cold start: do not
          reload them here."
        - "Ignore `superseded` and `archived` memory unless the user asks for
          history" — never enter normal retrieval.
        - Selection is filtered by the RESOLVED ENTITY (not a domain allowlist;
          domain-isolation-audit, DEFAULT/Context): a candidate's declared
          `area`, when present, must match the active entity's area; its
          load_policy trigger must match the active entity/intent.
        - Preferences are never retrieved here: "Las preferencias Meli y
          Aranea son scoped; se cargan solo con esas entidades" (perfil) and
          the routers load them via Minimal Reads only (C11).
        """
        if self.active_entity is None:
            return []
        entity = self.active_entity
        selected: List[str] = []
        mem_root = self.vault.abspath("80-agents/memory")
        for dirpath, dirnames, filenames in os.walk(mem_root):
            dirnames[:] = [d for d in sorted(dirnames) if not d.startswith(".")]
            for fn in sorted(filenames):
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), self.vault.root).replace(os.sep, "/")
                fm = self.vault.frontmatter(rel)
                state = str(fm.get("memory_state", "")).strip().strip("\"'").lower()
                if rel in self.all_opens():
                    continue  # already in context from cold start
                if state in ("superseded", "archived") and not explicit_history:
                    continue  # context-retrieval paso 5 / bootstrap Hard Rules
                if not trigger_fires(fm, entity, intent):
                    continue
                selected.append(rel)
        # NOTE: candidates are returned, NOT opened as bodies. context-
        # retrieval Hard Rules: "Do not load a note body without a prior
        # selection"; the scenario opens exactly the delta its turn declares
        # via open_delta().
        return sorted(selected)

    def open_delta(self, rel: str) -> Optional[str]:
        """Load the body of ONE previously selected candidate (the turn's
        declared delta). Returns the rel when the file is missing."""
        return self.open(rel, "cuerpo del delta seleccionado por retrieval")

    # -- entity swap (bootstrap entity swap pasos 1-4) ------------------------
    def swap_entity(self, title: str) -> Tuple[Optional[Entity], Optional[str]]:
        """Entity swap transcription:
        1. Keep the invariants and global internal note from cold start (no
           re-read; Session Modes: "skip global internal reload if already
           loaded this session").
        2. Resolve the new entity.
        3. Re-apply the domain gate with the new entity's `area`; if the domain
           changed, DROP the previous domain pack (router + scoped preferences)
           and load the new router. "Never hold two domain packs at once."
        4. Drop the previous entity pack from active reasoning (specialist
           skills go with the pack).

        Turn convention: does NOT advance the turn; every open performed here
        (new pack) is attributed to the turn the caller declared, so the
        scenario's per-turn assertions observe the actual swap turn."""
        prev_domain = self.active_domain
        prev_pack = list(self.pack_files)
        prev_specialists = list(self.specialist_skills)
        entity = self.vault.resolve_entity(title) if title else None
        old_entity = self.active_entity
        self.active_entity = entity
        if entity is not None:
            self._ensure_registry()
        domain, note = domain_gate(entity)
        self.gate_note = note
        # swap paso 3: drop the previous pack BEFORE loading the new one.
        dropped = prev_pack if domain != prev_domain else []
        self.pack_files = [f for f in self.pack_files if f not in dropped]
        self.specialist_skills = [s for s in self.specialist_skills if s not in prev_specialists] if domain != prev_domain else self.specialist_skills
        self._specialist_loaded = False
        if domain and domain != prev_domain:
            self._load_domain_pack(domain)
        elif not domain:
            self.pack_files = []
            self.active_domain = None
        self.session_mode = "entity-swap"
        self.swap_note = "pack anterior (%s) descartado; pack nuevo (%s) cargado; base sin relectura (bootstrap swap pasos 1-4)" % (
            prev_domain or "none", self.active_domain or "none")
        return old_entity, prev_domain

    # -- frontier rule (meli-agent-dev Hard Rules; C13) -----------------------
    def aranea_tool_decision(self, target: str) -> Tuple[str, str]:
        """Las capabilities MCP `aranea-*` "no existen en este dominio" para
        Meli: nunca usarlas para hosts, datos, repos o infraestructura
        Meli/corporativa (meli-agent-dev Hard Rules). Decision only — the
        harness never invokes tools (spec section 7). Presence of the tools on
        the surface is NOT a violation (domain-isolation-audit Hallazgo 4)."""
        if self.active_domain == "meli":
            return "no-invoke", "aranea-* no existen en el dominio meli (meli-agent-dev Hard Rules); presencia en superficie no es violacion (Hallazgo 4)"
        if self.active_domain == "aranea":
            if target == "meli":
                return "reject", "target Meli/corporativo se rechaza y deriva a meli-agent-dev antes de abrir conexiones (aranea-agent-dev Procedure 1)"
            return "requires-expert", "todo acceso aranea-* pasa por aranea-mcps-expert (aranea-agent-dev Hard Rules)"
        return "no-domain", "sin dominio activo no hay acceso MCP de dominio"

    # -- introspection ---------------------------------------------------------
    def domain_pack(self) -> List[str]:
        return list(self.pack_files)

    def holds_two_packs(self) -> bool:
        """Hard Rule: never hold two domain packs at once."""
        routers = [r for r in self.pack_files if r in set(ROUTERS.values())]
        return len(routers) > 1


# ---------------------------------------------------------------------------
# Retrieval trigger semantics (C09 + agents-os-context-retrieval paso 5).
# ---------------------------------------------------------------------------
def fm_list(value: object) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def references_entity(value: object, entity: Entity) -> bool:
    """Deterministic entity-reference match: canonical title, slug, alias, or
    slug-prefixed application (e.g. application [[rio-playmaker]] references
    entity RIO whose slug is 'rio'). Word-boundary title match for prose-ish
    project titles. This is the harness's documented operationalization of
    'matching trigger' — the exact 'error matching' semantics have no
    authority-defined threshold (contract-audit C09 Unknown)."""
    title = str(entity.get("title", ""))
    slug = str(entity.get("slug", "")).lower()
    aliases = [str(a).lower() for a in entity.get("aliases", [])]
    for raw in fm_list(value):
        v = raw.strip().strip("[[]]").strip().strip("\"'").lower()
        if not v:
            continue
        if title and (v == title.lower() or re.search(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(title.lower()), v)):
            return True
        if slug and (v == slug or v.startswith(slug + "-") or slug + "/" in v):
            return True
        for alias in aliases:
            # word-boundary alias match (a bare alias substring would make any
            # string containing it a reference, e.g. 'rio' inside
            # 'rio-controlplane-kafka' linked from another domain's note).
            if alias and re.search(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(alias), v):
                return True
    return False


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def trigger_fires(fm: Dict[str, object], entity: Entity, intent: str) -> bool:
    """Does this note's load_policy trigger fire for the active entity/intent?

    Authorities: schema-contract ("concrete runtime trigger"); bootstrap Hard
    Rules enumeration (when_project_loaded/when_application_loaded/
    when_error_matches/manual); constitucion ("when_*_loaded o manual"); the
    ad-hoc when_*_loaded values in the corpus (when_echo_forge_loaded, etc.)
    fit the constitucional when_*_loaded pattern but not bootstrap's literal
    enumeration — that tension is C09/LOAD-POLICY-VOCABULARY WARN and is
    reproduced here, not resolved (the trigger still fires on the pattern
    reading; the vocabulary finding is registered statically by L0)."""
    lp = str(fm.get("load_policy", "")).strip().strip("\"'").lower()
    if not lp or lp == "manual" or lp == "never":
        return False  # manual requires explicit invocation; never excludes runtime
    # Domain scoping (UNRELATED-DOMAIN-NOT-LOADED: the harness compares each
    # candidate against the DOMAIN of the active entity's area). Drift values
    # like [[Echo Forge]] map to no gate domain: the guard does not fire on
    # them (entity-reference matching decides) and the drift itself is
    # registered by L0 ACTIVE-MEMORY-DOMAIN-PURITY (Hallazgo 11), not silently
    # resolved here.
    e_dom = domain_from_area(entity.get("area"))
    n_dom = domain_from_area(fm.get("area"))
    if e_dom and n_dom and n_dom != e_dom:
        return False
    e_area = normalize_area(entity.get("area"))
    n_area = normalize_area(fm.get("area"))
    if lp == "when_area_loaded":
        return n_area is not None and e_area is not None and n_area == e_area
    # Entity-resolution fields only: entities/project/application. `related`
    # is a general link field and leaks cross-domain references (e.g. a symphony
    # decision linking [[rio-controlplane-*]] would otherwise match entity RIO).
    refs = (fm.get("entities"), fm.get("project"), fm.get("application"))
    ref_hit = any(references_entity(v, entity) for v in refs)
    if lp == "when_error_matches":
        # No authority defines what counts as "error matching" (C09 Unknown);
        # the harness applies entity-scoped matching for any retrieval intent.
        return ref_hit
    if lp == "when_project_loaded":
        return intent in ("context", "continuity", "error") and ref_hit
    if lp == "when_application_loaded":
        return intent in ("context", "continuity", "error") and ref_hit
    if lp.startswith("when_") and lp.endswith("_loaded"):
        # Generic constitucional when_*_loaded pattern reading (C09 WARN):
        # ad-hoc trigger key must equal the slugified canonical entity title.
        key = lp[len("when_"):-len("_loaded")].replace("_", "-")
        return intent in ("context", "continuity", "error") and slugify(str(entity.get("title", ""))) == key
    return False  # unknown trigger: fails closed (spec section 5 semantics)


# ---------------------------------------------------------------------------
# Fidelity anchors (adversarial-verification D2: guard against silent
# transcription drift). Each entry is (anchor_id, authority_rel_path, quote):
# the EXACT quote of the authority text that a rule of this module claims to
# transcribe. The harness pre-flight check RULES-FIDELITY-ANCHORS asserts that
# every quote still exists verbatim in the authority file (matching collapses
# whitespace runs only — the words must be exact). If an anchor disappears the
# transcription is stale and the results of gate-dependent scenarios are not
# trustworthy. When transcribing a NEW authority rule here, add its anchor.
# ---------------------------------------------------------------------------
AUTH_BOOTSTRAP = "80-agents/skills/agents-os-bootstrap/SKILL.md"
AUTH_DOCTOR = "80-agents/skills/agents-os-doctor/SKILL.md"

FIDELITY_ANCHORS: List[Tuple[str, str, str]] = [
    # Domain gate (bootstrap cold start paso 6) — cited at domain_gate().
    ("gate-registry", AUTH_BOOTSTRAP, "Apply the domain gate from the optional federated registry `30-resources/agents/domain-router-registry.md`"),
    ("gate-area", AUTH_BOOTSTRAP, "compare it exactly with the registry rows."),
    ("gate-task-evidence", AUTH_BOOTSTRAP, "Mere ambient tool availability is not task evidence."),
    ("gate-cardinality", AUTH_BOOTSTRAP, "Zero matches means DEFAULT with no domain router; one match loads exactly that router; more than one match fails closed and loads none."),
    ("gate-empty-registry", AUTH_BOOTSTRAP, "A missing or empty registry is a valid DEFAULT installation."),
    ("gate-one-specialist", AUTH_BOOTSTRAP, "The selected router loads at most ONE specialized skill and owns its scoped preferences."),
    # Cold set (bootstrap cold start pasos 1-5) — cited at Session.cold_start().
    ("cold-paso1-constitution", AUTH_BOOTSTRAP, "`80-agents/agents-os/agent-constitution.md`"),
    ("cold-paso1-profile-dir", AUTH_BOOTSTRAP, "`80-agents/memory/public/user-preference/` — the global profile. Resolve it by that directory"),
    ("cold-paso2-global-internal", AUTH_BOOTSTRAP, "`80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`"),
    ("cold-paso3-registry", AUTH_BOOTSTRAP, "Load the skills registry `80-agents/skills/INDEX.md` (core catalog + federated rows)"),
    ("cold-paso3-no-federated-index", AUTH_BOOTSTRAP, "Do not read the federated domain index unless routing needs detail beyond the registry rows."),
    ("cold-paso4-map-no-ritual", AUTH_BOOTSTRAP, "Read `agents-os.md` only if the task needs the conceptual map; do not add it to the base stack by ritual."),
    ("cold-paso5-resolve-aliases", AUTH_BOOTSTRAP, "Resolve aliases/slugs to the canonical Obsidian title."),
    # Warm turn (Session Modes + bootstrap warm pasos 1-4) — cited at Session.warm_turn().
    ("warm-reuse-delta-only", AUTH_BOOTSTRAP, "Reuse what is already in context. Fetch only the delta needed."),
    ("warm-never-reread", AUTH_BOOTSTRAP, "Never re-read constitution/profile/bootstrap."),
    ("warm-no-bootstrap-rerun", AUTH_BOOTSTRAP, "Do not invoke or reread bootstrap merely because the user sent another message."),
    # Entity swap (Session Modes + bootstrap swap pasos 1-4) — cited at Session.swap_entity().
    ("swap-skip-global-internal-reload", AUTH_BOOTSTRAP, "skip global internal reload if already loaded this session."),
    ("swap-keep-invariants", AUTH_BOOTSTRAP, "Keep the invariants and global internal note from cold start."),
    ("swap-drop-pack", AUTH_BOOTSTRAP, "drop the previous domain pack (router + scoped preferences) and load the new router. Never hold two domain packs at once."),
    # Superseded/archived exclusion — cited at Session.retrieve().
    ("hard-superseded-not-loaded", AUTH_BOOTSTRAP, "Never load `superseded` or `archived` continuity during normal startup or entity retrieval."),
    # Only startup procedure — cited by the L0 STARTUP-DUPLICATION contract.
    ("hard-only-startup-procedure", AUTH_BOOTSTRAP, "This skill is the only startup procedure. Do not duplicate it in `agents-os.md`, `AGENTS.md`, adapters, or project notes."),
    # doctor Check 3: closed club lines — cited at resolve_profile_note() and
    # the L0 CLOSED-CLUB-ALWAYS check.
    ("doctor-club-constitution", AUTH_DOCTOR, "`80-agents/agents-os/agent-constitution.md`"),
    ("doctor-club-bootstrap", AUTH_DOCTOR, "`80-agents/skills/agents-os-bootstrap/SKILL.md`"),
    ("doctor-club-global-internal", AUTH_DOCTOR, "`80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`"),
    ("doctor-club-one-profile", AUTH_DOCTOR, "exactly ONE note under `80-agents/memory/public/user-preference/` — the global profile."),
    ("doctor-club-second-is-violation", AUTH_DOCTOR, "a second one is a club violation and zero means the install is incomplete."),
]
