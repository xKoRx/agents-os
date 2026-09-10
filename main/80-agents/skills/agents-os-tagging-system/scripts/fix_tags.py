#!/usr/bin/env python3
import os
import re
import sys

def slugify(text):
    text = re.sub(r'\[\[(.*?)\]\]', r'\1', text)
    if '|' in text:
        text = text.split('|')[0]
    text = text.lower().strip()
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

def parse_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None, None
    
    yaml_text = match.group(1)
    data = {}
    
    current_key = None
    for line in yaml_text.split('\n'):
        # Strip comments
        if '#' in line:
            if not (line.strip().startswith('"') or line.strip().startswith("'")):
                line = line.split('#', 1)[0]
                
        stripped = line.strip()
        if not stripped:
            continue
            
        # Check if list item
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
                
    # Explicitly check for block tags block to be safe
    tags_match = re.search(r'^tags:\s*\n((?:\s*-\s*\S+\n?)+)', yaml_text, re.MULTILINE)
    if tags_match:
        tags_block = tags_match.group(1)
        tags = []
        for line in tags_block.split('\n'):
            line = line.strip()
            if line.startswith('-'):
                tags.append(line.replace('-', '').strip().strip('"\''))
        data['tags'] = tags
        
    return data, yaml_text

def build_new_frontmatter(data, original_yaml_text):
    lines = []
    keys_written = set()
    
    in_tags = False
    for line in original_yaml_text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('tags:'):
            in_tags = True
            lines.append("tags:")
            for tag in data.get('tags', []):
                lines.append(f"  - {tag}")
            keys_written.add('tags')
            continue
            
        if in_tags:
            if stripped.startswith('-'):
                continue
            else:
                in_tags = False
                
        if ':' in line and not in_tags:
            key = line.split(':', 1)[0].strip()
            if key in keys_written:
                continue
            lines.append(line)
            keys_written.add(key)
        else:
            if not in_tags:
                lines.append(line)
                
    if 'tags' not in keys_written and 'tags' in data:
        lines.append("tags:")
        for tag in data['tags']:
            lines.append(f"  - {tag}")
            
    return "---\n" + "\n".join(lines) + "\n---\n"

def fix_file_tags(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"

    frontmatter, original_yaml = parse_frontmatter(content)
    if not frontmatter:
        return False, "No frontmatter found"
    
    # Get values
    note_type = frontmatter.get('type')
    scope = frontmatter.get('scope')
    area = frontmatter.get('area')
    project = frontmatter.get('project')
    app = frontmatter.get('application')
    
    tags = frontmatter.get('tags', [])
    if not isinstance(tags, list):
        tags = [tags] if tags else []
        
    original_tags = list(tags)
    
    # Step 1: Ensure required namespaces
    if note_type:
        expected_kind_tag = f"kind/{slugify(note_type)}"
        if expected_kind_tag not in tags:
            tags.append(expected_kind_tag)
            
    if scope:
        expected_scope_tag = f"scope/{slugify(scope)}"
        if expected_scope_tag not in tags:
            tags.append(expected_scope_tag)
            
    # Step 2: Ensure recommended namespaces
    if area:
        areas = area if isinstance(area, list) else [area]
        for a in areas:
            a_slug = slugify(a)
            if a_slug:
                expected_area_tag = f"area/{a_slug}"
                if expected_area_tag not in tags:
                    tags.append(expected_area_tag)
                    
    if project:
        projects = project if isinstance(project, list) else [project]
        for p in projects:
            p_slug = slugify(p)
            if p_slug:
                expected_proj_tag = f"project/{p_slug}"
                if expected_proj_tag not in tags:
                    tags.append(expected_proj_tag)
                    
    if app:
        apps = app if isinstance(app, list) else [app]
        for ap in apps:
            ap_slug = slugify(ap)
            if ap_slug:
                expected_app_tag = f"app/{ap_slug}"
                if expected_app_tag not in tags:
                    tags.append(expected_app_tag)
                    
    # Step 3: Map flat tags to namespaced equivalents and remove duplicates/flats
    new_tags = []
    flat_mappings = {
        'application': 'kind/application',
        'runbook': 'kind/runbook',
        'meeting': 'kind/meeting',
        'project': 'kind/project',
        'area': 'kind/area',
        'learning': 'kind/learning',
        'decision': 'kind/decision',
        'known-error': 'kind/known-error',
        'known_error': 'kind/known-error',
        'change-log': 'kind/change-log',
        'change_log': 'kind/change-log',
        'session': 'kind/session',
        'raw-session': 'kind/raw-session',
        'raw_session': 'kind/raw-session',
        'system': 'kind/system',
        'agentsos': 'tech/agents-os',
        'agents-os': 'tech/agents-os',
        'skills': 'tech/skills',
        'skill': 'tech/skills',
        'tool': 'kind/tool',
        'resource': 'kind/resource',
        'doc': 'kind/doc'
    }
    
    for tag in tags:
        tag_cleaned = tag.strip().lower()
        if tag_cleaned in flat_mappings:
            mapped_tag = flat_mappings[tag_cleaned]
            if mapped_tag not in new_tags:
                new_tags.append(mapped_tag)
        else:
            if tag not in new_tags:
                new_tags.append(tag)
                
    # Filter out flat tags that are now mapped
    final_tags = []
    for tag in new_tags:
        if '/' in tag:
            if tag not in final_tags:
                final_tags.append(tag)
        else:
            if tag not in final_tags:
                final_tags.append(tag)

    # Sort tags
    final_tags.sort()
    
    if final_tags == original_tags:
        return False, "No changes needed"
        
    frontmatter['tags'] = final_tags
    
    # Rebuild YAML
    new_yaml = build_new_frontmatter(frontmatter, original_yaml)
    
    # Replace in file content
    new_content = content.replace(f"---\n{original_yaml}\n---", new_yaml.strip())
    if new_content == content:
        new_content = re.sub(r'^---\s*\n.*?\n---\s*\n', new_yaml, content, flags=re.DOTALL)
        
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, f"Updated tags: {original_tags} -> {final_tags}"
    except Exception as e:
        return False, f"Error writing file: {e}"

def main():
    vault_path = os.getcwd()
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
        
    print(f"Auto-fixing frontmatter tags in: {vault_path}")
    
    exclude_dirs = {'.obsidian', '.trash', 'graphify-out', '95-graphify', 'Excalidraw'}
    
    total_files = 0
    files_fixed = 0
    
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # Skip shared files or subfolders of skills
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
            
            # Skip templates dir
            if '70-templates/' in rel_path or '80-agents/templates/' in rel_path:
                continue
            if file == 'SKILL.md' or file == 'AGENTS.md':
                continue
                
            success, msg = fix_file_tags(filepath)
            if success:
                files_fixed += 1
                print(f"✔ Fixed: {rel_path} - {msg}")
            total_files += 1
            
    print("\n--- Fix Summary ---")
    print(f"Total files checked: {total_files}")
    print(f"Total files auto-fixed: {files_fixed}")

if __name__ == '__main__':
    main()
