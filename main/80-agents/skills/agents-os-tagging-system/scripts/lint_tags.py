#!/usr/bin/env python3
import os
import re
import sys

def parse_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None
    
    yaml_text = match.group(1)
    data = {}
    
    current_key = None
    for line in yaml_text.split('\n'):
        if '#' in line:
            if not (line.strip().startswith('"') or line.strip().startswith("'")):
                line = line.split('#', 1)[0]
                
        stripped = line.strip()
        if not stripped:
            continue
            
        if stripped.startswith('-') and current_key:
            val = stripped[1:].strip().strip('"\'')
            if current_key not in data:
                data[current_key] = []
            elif not isinstance(data[current_key], list):
                data[current_key] = [data[current_key]]
            data[current_key].append(val)
            continue
            
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"\'')
            current_key = key
            
            if val == '':
                data[key] = []
            elif val.startswith('[') and val.endswith(']') and not (val.startswith('[[') and val.endswith(']]')):
                val_list = [v.strip('"\' ') for v in val[1:-1].split(',')]
                data[key] = [v for v in val_list if v]
            else:
                data[key] = val
                
    return data

def slugify(text):
    text = re.sub(r'\[\[(.*?)\]\]', r'\1', text)
    if '|' in text:
        text = text.split('|')[0]
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text

def lint_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"Error reading file: {e}"]

    frontmatter = parse_frontmatter(content)
    if not frontmatter:
        if content.strip().startswith('# '):
            return [f"Missing frontmatter/YAML block"]
        return []
    
    errors = []
    
    # Rule 1: Must have type
    note_type = frontmatter.get('type')
    if not note_type:
        errors.append("Missing 'type' field in frontmatter")
    
    # Rule 2: Must have scope for memory types
    scope = frontmatter.get('scope')
    if not scope:
        memory_types = ['learning', 'decision', 'known_error', 'runbook', 'command', 'pattern', 'change_log']
        if note_type in memory_types:
            errors.append(f"Memory type '{note_type}' is missing 'scope' field")
            
    tags = frontmatter.get('tags', [])
    if not isinstance(tags, list):
        tags = [tags] if tags else []
        
    # Rule 3: kind/<type> tag must match type
    if note_type:
        expected_kind_tag = f"kind/{slugify(note_type)}"
        if expected_kind_tag not in tags:
            errors.append(f"Missing required tag '{expected_kind_tag}' matching type '{note_type}'")
            
    # Rule 4: scope/<scope> tag must match scope
    if scope:
        expected_scope_tag = f"scope/{slugify(scope)}"
        if expected_scope_tag not in tags:
            errors.append(f"Missing required tag '{expected_scope_tag}' matching scope '{scope}'")
            
    # Rule 5: area/<area-slug> must match area field
    area = frontmatter.get('area')
    if area:
        areas = area if isinstance(area, list) else [area]
        for a in areas:
            a_slug = slugify(a)
            if a_slug:
                expected_area_tag = f"area/{a_slug}"
                if expected_area_tag not in tags:
                    errors.append(f"Missing recommended tag '{expected_area_tag}' matching area '{a}'")
                    
    # Rule 6: project/<project-slug> must match project field
    project = frontmatter.get('project')
    if project:
        projects = project if isinstance(project, list) else [project]
        for p in projects:
            p_slug = slugify(p)
            if p_slug:
                expected_proj_tag = f"project/{p_slug}"
                if expected_proj_tag not in tags:
                    errors.append(f"Missing recommended tag '{expected_proj_tag}' matching project '{p}'")

    # Rule 7: application/<app-slug> or app/<app-slug> matching
    app = frontmatter.get('application')
    if app:
        apps = app if isinstance(app, list) else [app]
        for ap in apps:
            ap_slug = slugify(ap)
            if ap_slug:
                expected_app_tag = f"app/{ap_slug}"
                if expected_app_tag not in tags:
                    errors.append(f"Missing recommended tag '{expected_app_tag}' matching application '{ap}'")

    # Rule 8: Flat tags check (no namespacing)
    for tag in tags:
        # Let 'project' and 'area' in root entities slide, but check namespacing
        if '/' not in tag:
            # Skip if it is project or area tag which are standard in project/area notes
            if tag in ['project', 'area', 'sprint', 'quarter', 'index']:
                continue
            errors.append(f"Flat tag '{tag}' found. Consider using namespaces (e.g. tech/{tag} or kind/{tag})")

    return errors

def main():
    vault_path = os.getcwd()
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
        
    print(f"Linting frontmatter tags in: {vault_path}")
    
    exclude_dirs = {'.obsidian', '.trash', 'graphify-out', '95-graphify', 'Excalidraw', '90-system', '00-inbox'}
    
    total_files = 0
    files_with_errors = 0
    total_errors = 0
    
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        rel_root = os.path.relpath(root, vault_path)
        if '80-agents/skills/' in rel_root and rel_root != '80-agents/skills':
            continue
        if '_shared' in rel_root:
            continue
            
        for file in files:
            if not file.endswith('.md'):
                continue
                
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, vault_path)
            
            # Skip root files like README.md
            if os.path.dirname(rel_path) == '':
                continue
            if '70-templates/' in rel_path or '80-agents/templates/' in rel_path:
                continue
            if file == 'SKILL.md' or file == 'AGENTS.md':
                continue
                
            errors = lint_file(filepath)
            if errors:
                files_with_errors += 1
                total_errors += len(errors)
                print(f"\n❌ {rel_path}:")
                for err in errors:
                    print(f"  - {err}")
            total_files += 1
            
    print("\n--- Summary ---")
    print(f"Total files checked: {total_files}")
    print(f"Files with errors: {files_with_errors}")
    print(f"Total errors found: {total_errors}")
    
    if total_errors > 0:
        sys.exit(1)
    else:
        print("All checks passed! 🎉")
        sys.exit(0)

if __name__ == '__main__':
    main()
