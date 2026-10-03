from pathlib import Path
import hashlib,json,os
root=Path('/private/tmp/kafka-e2e-discovery/cp-ci-scope-control-author')
plan=json.loads((root/'publication-plan.json').read_text())
target=Path(plan['target']); candidate=root/'e2e/tests/ci-family-scope-contract.py'; backup=Path(plan['backup_guard']['new_source_backup'])
assert str(target)=='/Users/rjara/fuentes/rio-controlplane-kafka-e2e/e2e/tests/ci-family-scope-contract.py'
assert not os.path.lexists(target) and not target.parent.is_symlink()
expected=plan['backup_guard']['new_source_sha256']
assert hashlib.sha256(candidate.read_bytes()).hexdigest()==expected and hashlib.sha256(backup.read_bytes()).hexdigest()==expected
assert hashlib.sha256(Path('/Users/rjara/fuentes/rio-controlplane-kafka-e2e/e2e/ci.sh').read_bytes()).hexdigest()==plan['backup_guard']['CI_after_sha256']
compile(candidate.read_bytes(),str(candidate),'exec')
descriptor=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
with os.fdopen(descriptor,'wb') as output:
    output.write(candidate.read_bytes()); output.flush(); os.fsync(output.fileno())
descriptor=os.open(target.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
try: os.fsync(descriptor)
finally: os.close(descriptor)
assert hashlib.sha256(target.read_bytes()).hexdigest()==expected
receipt={'target':str(target),'before':'ABSENT','after_sha256':expected,'backup':str(backup),'writes':'EXACT_ONE_NEW_AUTHORIZED_FILE','remote_API_calls':0,'Docker':0,'Gradle':0,'commits':0,'business':'NOT_EXECUTED'}
(root/'publication-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PUBLISHED_ONE_NEW_FILE',expected)
