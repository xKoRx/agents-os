from pathlib import Path
import hashlib,json,os,stat,tempfile
root=Path('/private/tmp/kafka-e2e-discovery/cp-only-sandbox-author')
plan=json.loads((root/'publication-plan.json').read_text())
allowed={'/Users/rjara/fuentes/rio-controlplane-kafka-e2e/e2e/sandbox.py','/Users/rjara/fuentes/rio-controlplane-kafka-e2e/e2e/tests/sandbox-contract.py'}
assert {record['path'] for record in plan['files']}==allowed and len(plan['files'])==2
for record in plan['files']:
    target=Path(record['path']); backup=Path(record['backup']); candidate=Path(record['candidate'])
    assert not target.is_symlink() and hashlib.sha256(target.read_bytes()).hexdigest()==record['before_sha256']
    assert hashlib.sha256(backup.read_bytes()).hexdigest()==record['before_sha256']
    assert hashlib.sha256(candidate.read_bytes()).hexdigest()==record['after_sha256']
    assert stat.S_IMODE(target.stat().st_mode)==record['mode']
for record in plan['files']:
    target=Path(record['path']); payload=Path(record['candidate']).read_bytes()
    descriptor,temporary=tempfile.mkstemp(prefix=target.name+'.cp-scope-',dir=target.parent)
    try:
        with os.fdopen(descriptor,'wb') as output:
            os.fchmod(output.fileno(),record['mode']); output.write(payload); output.flush(); os.fsync(output.fileno())
        os.replace(temporary,target)
        directory=os.open(target.parent,os.O_RDONLY)
        try: os.fsync(directory)
        finally: os.close(directory)
    finally: Path(temporary).unlink(missing_ok=True)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==record['after_sha256']
receipt={'verdict':'PUBLISHED_EXACT_TWO_AUTHORIZED_FILES','files':plan['files'],'remote_API_calls':0,'Docker':0,'Gradle':0,'commits':0,'business':'NOT_EXECUTED'}
path=root/'publication-receipt.json'; path.write_text(json.dumps(receipt,indent=2)+'\n'); os.chmod(path,0o600)
print(receipt['verdict'])
for record in plan['files']: print(record['relative'],record['after_sha256'])
