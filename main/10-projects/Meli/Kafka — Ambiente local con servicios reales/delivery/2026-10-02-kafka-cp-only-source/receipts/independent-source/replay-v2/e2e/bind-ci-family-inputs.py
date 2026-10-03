#!/usr/bin/env python3
"""Bind private input bytes to an isolated CI run; never establish service or grant authority."""
import argparse
import base64
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from urllib.parse import urlsplit

SOURCE = '25b34c73b97327ad2f247689dd5e660e0d209b5b'
MAX_BYTES = 1_048_576
POINTERS = ('deployment_pointer', 'source_pointer', 'base_url_pointer', 'scope_pointer',
            'release_pointer', 'active_pointer', 'application_pointer')


def require(condition, code):
    if not condition:
        raise ValueError('CI_INPUT_BINDING:' + code)


def directory(path):
    require(path.is_absolute() and not any(item.is_symlink() for item in (path, *path.parents)), 'DIRECTORY')
    actual = path.stat()
    require(stat.S_ISDIR(actual.st_mode) and actual.st_uid == os.getuid()
            and stat.S_IMODE(actual.st_mode) == 0o700, 'DIRECTORY')


def read_private(path):
    directory(path.parent)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        actual = os.fstat(descriptor)
        require(stat.S_ISREG(actual.st_mode) and actual.st_uid == os.getuid()
                and stat.S_IMODE(actual.st_mode) == 0o600 and actual.st_size <= MAX_BYTES, 'FILE')
        with os.fdopen(os.dup(descriptor), 'rb') as source:
            raw = source.read(MAX_BYTES + 1)
        require(len(raw) <= MAX_BYTES, 'SIZE')
        current = path.stat(follow_symlinks=False)
        require((actual.st_dev, actual.st_ino) == (current.st_dev, current.st_ino), 'FILE_REPLACED')
        return raw
    finally:
        os.close(descriptor)


def unique_object(pairs):
    document = {}
    for name, value in pairs:
        require(name not in document, 'DUPLICATE_JSON_FIELD')
        document[name] = value
    return document


def decode(raw):
    value = json.loads(raw, object_pairs_hook=unique_object)
    require(isinstance(value, dict), 'JSON_OBJECT')
    return value


def write_private(path, raw):
    directory(path.parent)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(os.dup(descriptor), 'wb') as destination:
            destination.write(raw)
            destination.flush()
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def reference(raw, binding, name):
    expected = binding[name].get('sha256')
    require(isinstance(expected, str) and re.fullmatch('[a-f0-9]{64}', expected)
            and hashlib.sha256(raw).hexdigest() == expected, 'REFERENCE_HASH')
    document = decode(raw)
    require(document.get('status') == 200 and isinstance(document.get('request_uri'), str)
            and bool(document['request_uri']) and re.fullmatch('[a-f0-9]{64}', str(document.get('body_sha256', ''))),
            'REFERENCE_RESPONSE')
    if name == 'runtime_ref':
        require(document['request_uri'] == 'deployments?application=rio-entity-service&active=true', 'DEPLOYMENT_ROUTE')
    return raw


def validate_entity(binding):
    require(binding.get('source_commit') == SOURCE, 'ENTITY_SOURCE')
    target = urlsplit(binding.get('base_url', ''))
    require(target.scheme == 'https' and target.hostname and target.path == '' and not target.query
            and not target.fragment and target.username is None and target.password is None, 'ENTITY_BASE')
    for name in ('runtime_ref', 'identity_ref'):
        require(isinstance(binding.get(name), dict), 'REFERENCE_OBJECT')
    for name in POINTERS:
        value = binding['runtime_ref'].get(name)
        require(isinstance(value, str) and value.startswith('/') and len(value) <= 512, 'DEPLOYMENT_POINTER')
    require(isinstance(binding.get('run_id'), str)
            and re.fullmatch('[a-z0-9][a-z0-9_-]{7,63}', binding['run_id']), 'TEMPLATE_RUN')
    require(binding.get('namespace') == 'rio.e2e.' + re.sub('[^a-z0-9]', '', binding['run_id']), 'TEMPLATE_NAMESPACE')
    require(isinstance(binding.get('team'), str) and bool(binding['team'])
            and str(binding.get('caller_mrn', '')).startswith('mrn:seginf:ad:user/'), 'IDENTITY_BINDING')
    require(re.fullmatch('[a-f0-9]{64}', str(binding.get('token_sha256', ''))), 'TOKEN_HASH')


def validate_denied(binding):
    token = binding.get('tiger_token')
    require(isinstance(token, str) and bool(token) and len(token) <= 16_384
            and not any(ord(character) < 32 or ord(character) == 127 for character in token), 'DENIED_TOKEN')
    token = token.removeprefix('Bearer ')
    require(hashlib.sha256(token.encode()).hexdigest() == binding.get('token_sha256')
            and str(binding.get('caller_mrn', '')).startswith('mrn:seginf:ad:user/'), 'DENIED_BINDING')


def bind(args):
    directory(args.directory)
    require(not any(args.directory.iterdir()), 'DESTINATION_NOT_FRESH')
    require(re.fullmatch('[a-f0-9]{32}', args.run), 'ACTUAL_SANDBOX_RUN_REQUIRED')
    entity_raw = read_private(args.entity_template)
    binding = decode(entity_raw)
    validate_entity(binding)
    references = {}
    for name in ('runtime_ref', 'identity_ref'):
        source = Path(binding[name]['path'])
        require(source.is_absolute() and source.parent == args.entity_template.parent, 'SIBLING_REFERENCE')
        references[name] = reference(read_private(source), binding, name)
    denied_raw = read_private(args.denied_template)
    denied = decode(denied_raw)
    validate_denied(denied)
    changed = copy.deepcopy(binding)
    changed['run_id'] = args.run
    changed['namespace'] = 'rio.e2e.' + args.run
    for name, raw in references.items():
        target = args.directory / (name + '.json')
        write_private(target, raw)
        changed[name]['path'] = str(target)
    changed_denied = copy.deepcopy(denied)
    changed_denied['run_id'] = args.run
    write_private(args.directory / 'entity-receipt.json', encoded(changed))
    write_private(args.directory / 'denied-identity.json', encoded(changed_denied))
    # This receipt is a binding transformation only; fresh Fury/Tiger/ACME proof remains mandatory.
    manifest = {'schema_version': 1, 'kind': 'PRIVATE_INPUT_BINDING_ONLY', 'run_id': args.run,
                'source_commit': SOURCE, 'template_sha256': hashlib.sha256(entity_raw).hexdigest(),
                'denied_template_sha256': hashlib.sha256(denied_raw).hexdigest(),
                'reference_sha256': {name: hashlib.sha256(raw).hexdigest() for name, raw in references.items()}}
    write_private(args.directory / 'binding.json', encoded(manifest))


def stage(args):
    directory(args.directory)
    require(not any(args.directory.iterdir()), 'DESTINATION_NOT_FRESH')
    for value_name, filename in (('CALLER_CONFIG', 'caller.env'), ('MANAGED_CONFIG', 'managed.env'),
                                 ('MANAGED_KVS_CONFIG', 'managed-kvs.env')):
        content = os.environ.get(value_name, '')
        if content:
            require(len(content.encode()) <= MAX_BYTES, 'PRIVATE_CONFIG_SIZE')
            write_private(args.directory / filename, content.encode())
    denied_raw = os.environ.get('DENIED_TEMPLATE', '').encode()
    if denied_raw:
        validate_denied(decode(denied_raw))
        write_private(args.directory / 'denied-template.json', denied_raw)
    bundle = decode(os.environ['ENTITY_TEMPLATE_BUNDLE'].encode())
    require(set(bundle) == {'receipt', 'runtime_ref', 'identity_ref'}, 'BUNDLE_FIELDS')
    raw = {name: base64.b64decode(value, validate=True) for name, value in bundle.items()}
    require(all(len(value) <= MAX_BYTES for value in raw.values()), 'BUNDLE_SIZE')
    binding = decode(raw['receipt'])
    validate_entity(binding)
    for name in ('runtime_ref', 'identity_ref'):
        reference(raw[name], binding, name)
        path = args.directory / (name + '.json')
        write_private(path, raw[name])
        binding[name]['path'] = str(path)
    write_private(args.directory / 'entity-template.json', encoded(binding))


def read_run(args):
    values = {}
    for line in read_private(args.file).decode().splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        key, separator, value = line.partition('=')
        key = key.strip()
        require(separator and re.fullmatch('[A-Z][A-Z0-9_]*', key) and key not in values, 'ENV_FORMAT')
        value = value.strip()
        if value.startswith(('"', "'")):
            require(len(value) >= 2 and value[-1] == value[0], 'ENV_QUOTE')
            value = value[1:-1]
        require(not any(ord(character) < 32 or ord(character) == 127 for character in value), 'ENV_VALUE')
        values[key] = value
    value = values.get(args.name, '')
    require(re.fullmatch('[a-z0-9][a-z0-9_-]{7,63}', value), 'RUN_BINDING')
    print(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    binding = commands.add_parser('bind')
    binding.add_argument('--run', required=True)
    binding.add_argument('--directory', type=Path, required=True)
    binding.add_argument('--entity-template', type=Path, required=True)
    binding.add_argument('--denied-template', type=Path, required=True)
    staging = commands.add_parser('stage-workflow')
    staging.add_argument('--directory', type=Path, required=True)
    reader = commands.add_parser('read-run')
    reader.add_argument('--file', type=Path, required=True)
    reader.add_argument('--name', choices=('E2E_RUN_ID', 'E2E_MANAGED_RUN_ID'), required=True)
    args = parser.parse_args()
    {'bind': bind, 'stage-workflow': stage, 'read-run': read_run}[args.command](args)
    if args.command != 'read-run':
        print('CI_INPUT_BINDING_PASS:' + args.command)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError):
        print('CI_INPUT_BINDING_FAILED', file=__import__('sys').stderr)
        raise SystemExit(2)
