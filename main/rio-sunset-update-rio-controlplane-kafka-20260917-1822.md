# Rio sunset update — run report

- Project (exact Fury application name): `rio-controlplane-kafka`
- Executed at: `2026-09-17T18:22:46-03:00`
- Window evaluated (inclusive, execution day counts as day 1): `2026-09-17T00:00:00-03:00` through `2026-10-01T23:59:59.999-03:00`
- Timezone used: `America/Santiago` (`UTC-03:00` during the evaluated window)
- Run outcome: `stopped at phase 4 — classification: no mechanically safe applied items`
- Checkout: pre-existing at `/Users/rjara/fuentes/rio-controlplane-kafka`

## Mapped sunsets

| Sunset ID | Component/dependency | Expiry date | Previous version | Target version | Outcome | Managed by | Evidence reference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `5971996` | `org.springframework/spring-webmvc` | `2026-09-17T21:00:00.000-03:00` | `6.2.12` | `7.0.9` | Blocked: managed by a build plugin; a manager/compatibility decision is required | `org.springframework.boot` plugin `3.5.16`; manifest: `id 'org.springframework.boot' version '3.5.16'` (`build.gradle:2`) | [Fury artifact 202607.15.1](https://web.furycloud.io/engineering/applications/rio-controlplane-kafka/artifact-details/version/202607.15.1/detail) — `Arbitrary Code Injection`, SECURITY, CRITICAL, advisor `OSS` |
| `5972003` | `org.springframework/spring-webmvc` | `2026-09-17T21:00:00.000-03:00` | `6.2.19` | `7.0.9` | Blocked: managed by a build plugin; a manager/compatibility decision is required | `org.springframework.boot` plugin `3.5.16`; manifest: `id 'org.springframework.boot' version '3.5.16'` (`build.gradle:2`) | [Fury artifact 202609.17.0-rc-1](https://web.furycloud.io/engineering/applications/rio-controlplane-kafka/artifact-details/version/202609.17.0-rc-1/detail) — `Arbitrary Code Injection`, SECURITY, CRITICAL, advisor `OSS` |

The project demonstrates an override idiom at `build.gradle:41-44` through `configurations.configureEach { resolutionStrategy.force(...) }`. Applying a new Spring override still requires an explicit human decision under the skill because it would diverge from the plugin-managed dependency set. A non-persistent validation with `-Pspring-framework.version=7.0.9` resolved the target from the configured internal registry but failed 7 Spring integration tests with `NoSuchMethodError` in `SpringExtension`.

## Ya en curso — excluidos del lote

None detected. Open pull requests and recent Fury versions were reviewed. The current release candidate `202609.17.0-rc-1` still resolves `spring-webmvc` `6.2.19` and remains affected; no open PR or active recent branch moves the component to the stated target.

## Sunsets con fecha fuera de la ventana

| Sunset ID | Component/dependency | Expiry date | Current version | Target version | Days until expiry |
| --- | --- | --- | --- | --- | --- |
| `2565452` | `org.apache.kafka/kafka-clients` | `2026-05-14T20:00:00.000-04:00` | `3.9.1` | `3.9.2` | -126 |
| `420-1119976` | `com.mercadolibre.library/services-compression-java-tk` | `2026-05-31T11:00:00.000-04:00` | `0.0.1` | `1.1.1` | -109 |
| `419-1814010` | `com.mercadolibre/mqclient` | `2026-06-12T11:00:00.000-04:00` | `3.4.7` | `3.4.8` | -97 |
| `184-1498045` | `com.mercadolibre/mqclient` | `2026-07-06T11:00:00.000-04:00` | `3.4.5` | `3.4.8` | -73 |
| `2851878` | `io.opentelemetry/opentelemetry-api` | `2026-10-02T21:00:00.000-03:00` | `1.48.0` | `1.62.0` | 15 |
| `6436250` | `com.github.luben/zstd-jni` | `2026-10-10T21:00:00.000-03:00` | `1.5.6-4` | `1.5.7-14` | 23 |
| `6436394` | `com.github.luben/zstd-jni` | `2026-10-10T21:00:00.000-03:00` | `1.5.6-4` | `1.5.7-14` | 23 |
| `6436538` | `com.github.luben/zstd-jni` | `2026-10-10T21:00:00.000-03:00` | `1.5.6-4` | `1.5.7-14` | 23 |
| `6436625` | `com.github.luben/zstd-jni` | `2026-10-10T21:00:00.000-03:00` | `1.5.6-4` | `1.5.7-14` | 23 |
| `6436712` | `com.github.luben/zstd-jni` | `2026-10-10T21:00:00.000-03:00` | `1.5.6-4` | `1.5.7-14` | 23 |
| `593-704205` | `com.mercadolibre.library/java-melitk-autobulk-lib` | `2026-10-27T21:00:00.000-03:00` | `0.0.4` | `0.0.5` | 40 |
| `627-945726` | `com.mercadolibre.library/java-melitk-config` | `2026-10-27T21:00:00.000-03:00` | `0.5.0` | `2.0.0` | 40 |
| `739-1290104` | `com.fury.toolkit/java-toolkit-ad-watcher` | `2026-12-10T21:00:00.000-03:00` | `0.2.1` | `1.0.1` | 84 |
| `717-1488393` | `com.mercadolibre.json_jackson/json-jackson` | `2026-12-10T21:00:00.000-03:00` | `2.1.3` | `4.0.0` | 84 |
| `717-1488394` | `com.mercadolibre.json/json-core` | `2026-12-10T21:00:00.000-03:00` | `2.1.3` | `4.0.0` | 84 |
| `718-1488395` | `com.mercadolibre.resilience/rate-limiter` | `2026-12-10T21:00:00.000-03:00` | `3.1.5` | `4.0.1` | 84 |
| `718-1488396` | `com.mercadolibre.resilience/resilience-core` | `2026-12-10T21:00:00.000-03:00` | `3.1.5` | `4.0.1` | 84 |
| `727-1488403` | `com.mercadolibre.restclient/meli-restclient-context` | `2026-12-10T21:00:00.000-03:00` | `3.1.2` | `4.0.0` | 84 |
| `727-1488404` | `com.mercadolibre.restclient/meli-restclient-core` | `2026-12-10T21:00:00.000-03:00` | `3.1.2` | `4.0.0` | 84 |
| `727-1488415` | `com.mercadolibre.restclient/meli-restclient-default` | `2026-12-10T21:00:00.000-03:00` | `3.1.2` | `4.0.0` | 84 |
| `733-1488401` | `com.mercadolibre.restclient/restclient-cache` | `2026-12-10T21:00:00.000-03:00` | `2.5.1` | `3.0.0` | 84 |
| `733-1488398` | `com.mercadolibre.restclient/restclient-core` | `2026-12-10T21:00:00.000-03:00` | `2.5.1` | `3.0.0` | 84 |
| `733-1488405` | `com.mercadolibre.restclient/restclient-default` | `2026-12-10T21:00:00.000-03:00` | `2.5.1` | `3.0.0` | 84 |
| `733-1488400` | `com.mercadolibre.restclient/restclient-default-parsers` | `2026-12-10T21:00:00.000-03:00` | `2.5.1` | `3.0.0` | 84 |
| `733-1488399` | `com.mercadolibre.restclient/restclient-http` | `2026-12-10T21:00:00.000-03:00` | `2.5.1` | `3.0.0` | 84 |
| `733-1488402` | `com.mercadolibre.restclient/restclient-httpc` | `2026-12-10T21:00:00.000-03:00` | `2.5.1` | `3.0.0` | 84 |
| `742-1497659` | `com.mercadolibre/kvsclient` | `2026-12-10T21:00:00.000-03:00` | `2.3.4` | `2.3.6` | 84 |
| `721-1488410` | `com.mercadolibre/routing` | `2026-12-10T21:00:00.000-03:00` | `3.1.3` | `4.0.2` | 84 |
| `720-1488417` | `com.mercadolibre/threading` | `2026-12-10T21:00:00.000-03:00` | `1.2.2` | `3.0.0` | 84 |
| `446-1837126` | `com.mercadolibre/mqclient` | `2027-05-03T09:14:53.000-04:00` | `3.4.8` | `3.4.9` | 228 |

## Pull request

| Field | Value |
| --- | --- |
| Pull request | Not created — stopped at phase 4 because both eligible items are plugin-managed and no item was safe to apply mechanically |
| Reused an existing open PR | No matching sunset PR exists |
| Base branch | `develop` |
| Applied sunset IDs | None |
| PR commit SHA | Not produced — no applied items |
| Immutable build for that SHA | Not produced — phase 7 was not reached |

- Files changed in the application checkout: none (`git status --porcelain` clean).
- Native project commands executed: `./gradlew --version`; `./gradlew dependencyInsight --dependency spring-webmvc --configuration runtimeClasspath`; `./gradlew -Pspring-framework.version=7.0.9 dependencyInsight --dependency spring-webmvc --configuration runtimeClasspath`; `./gradlew -Pspring-framework.version=7.0.9 test`.
- Validation results: Gradle `9.3.1` on Java `21.0.9`; current dependency resolves to `spring-webmvc 6.2.19`; target `7.0.9` exists and resolves from `JavaAll`; controlled target test run failed (`605` tests completed, `7` failed) with `NoSuchMethodError` in Spring test integration.

## Test deployment

Not performed. Build creation, scope selection, confirmation, and deploy were not reached because phase 4 produced no applied items. No production or test deployment, promotion, finish, terminate, or auto-merge was performed.

## Destino del documento

| Field | Value |
| --- | --- |
| Local path | `/Users/rjara/obsidian/SecondBrain/main/rio-sunset-update-rio-controlplane-kafka-20260917-1822.md` |
| Drive | Not configured in this run; local only |

## Notes and blocks

- Discovery covered all 6 deployed scopes, their 4 distinct artifact versions, and all catalog pages (`total_pages: 1` for each); 28 dependency/version entries carried sunset dates, representing 32 issue-level sunset items.
- The authenticated Fury UI was used as the initial fallback to inspect summary and consuming scopes; the authenticated Fury API was then used to normalize issue IDs and evidence without recording credentials or raw responses.
- Fury displays the two eligible deadlines as `17/09/2026`; the structured issue timestamp is `2026-09-18T00:00:00.000Z`, which is `2026-09-17T21:00:00.000-03:00` in the run timezone.
- A recent candidate build, `202609.17.0-rc-1`, carries `spring-webmvc 6.2.19`; it does not resolve sunset `5972003`.
- `graphify-out/` was preserved. The requested tracked `.gitignore` entry was not added because the skill prohibits opening a PR when the batch has no applied vulnerability item; it remains appropriate to include it when a valid vulnerability PR is authorized.
