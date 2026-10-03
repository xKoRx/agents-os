from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,stat,subprocess

ROOT=Path('/private/tmp/kafka-e2e-discovery/independent-review/cp-only-source-portability')
plan=json.loads((ROOT/'plan.json').read_text())
original_paths=[Path('/Users/rjara/fuentes/rio-controlplane-kafka'),Path('/Users/rjara/fuentes/rio-playmaker'),Path('/Users/rjara/fuentes/rio-sdk-events'),Path('/Users/rjara/fuentes/ads-signals-knowledge-library')]
source_paths=list(dict.fromkeys(Path(case['repo']) for case in plan['cases']))
environment={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0','GIT_LFS_SKIP_SMUDGE':'1'}
commands=[]

def git(arguments,cwd=None,record=True):
    command=['git','-c','core.hooksPath=/dev/null','-c','filter.lfs.required=false','-c','filter.lfs.smudge=','-c','filter.lfs.process=',*arguments]
    result=subprocess.run(command,cwd=cwd,env=environment,capture_output=True,timeout=60)
    if record:
        commands.append({'command':command,'cwd':str(cwd) if cwd else None,'exit':result.returncode,'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(result.stderr).hexdigest()})
    if result.returncode:
        raise RuntimeError('PORTABLE_COMMAND_FAILED:'+str(result.returncode)+':'+str(arguments))
    return result.stdout

def snapshot(path):
    gitprefix=['-C',str(path)]
    status=git([*gitprefix,'status','--porcelain=v1','-z','--untracked-files=all'],record=False)
    refs=git([*gitprefix,'for-each-ref','--format=%(refname)%00%(objectname)'],record=False)
    changes=hashlib.sha256()
    for label,arguments in [('status',['status','--porcelain=v1','-z','--untracked-files=all']),('unstaged',['diff','--binary','--no-ext-diff','--no-textconv']),('staged',['diff','--cached','--binary','--no-ext-diff','--no-textconv'])]:
        changes.update(label.encode()+b'\0'+git([*gitprefix,*arguments],record=False)+b'\0')
    untracked=git([*gitprefix,'ls-files','--others','--exclude-standard','-z'],record=False)
    for name in sorted(item for item in untracked.split(b'\0') if item):
        file=path/os.fsdecode(name)
        changes.update(name+b'\0')
        if file.is_symlink(): changes.update(b'symlink\0'+os.readlink(file).encode())
        elif file.is_file(): changes.update(b'file\0'+hashlib.sha256(file.read_bytes()).digest())
        else: changes.update(b'unsupported-kind\0')
        changes.update(b'\0')
    head=git([*gitprefix,'rev-parse','HEAD'],record=False).decode().strip()
    branch=subprocess.run(['git','-C',str(path),'symbolic-ref','-q','--short','HEAD'],env=environment,capture_output=True,timeout=10)
    return {'path':str(path),'head':head,'branch':branch.stdout.decode().strip() or 'DETACHED','refs_sha256':hashlib.sha256(refs).hexdigest(),'Git_visible_changes_sha256':changes.hexdigest(),'clean':status==b'','untracked_nonignored_count':len([name for name in untracked.split(b'\0') if name])}

clone_parent=ROOT/'private-clones'
clone_parent.mkdir(mode=0o700,exist_ok=False)
before={str(path):snapshot(path) for path in [*source_paths,*original_paths]}
results=[]; failures=[]; clones=[]
try:
    for case in plan['cases']:
        source=Path(case['repo']); expected=before[str(source)]
        assert expected['head']==case['head'] and expected['clean']
        patch=Path(case['patch']); payload=patch.read_bytes()
        assert hashlib.sha256(payload).hexdigest()==case['patch_sha256'] and len(payload)==case['bytes']
        clone=clone_parent/case['name']; assert not clone.exists(); clones.append(clone)
        git(['clone','--shared','--no-checkout','--',str(source),str(clone)])
        git(['checkout','--detach',case['base']],cwd=clone)
        assert git(['rev-parse','HEAD'],cwd=clone).decode().strip()==case['base']
        assert git(['status','--porcelain=v1','-z','--untracked-files=all'],cwd=clone)==b''
        git(['apply','--check','--index','--whitespace=nowarn',str(patch)],cwd=clone)
        git(['apply','--index','--whitespace=nowarn',str(patch)],cwd=clone)
        imported_tree=git(['write-tree'],cwd=clone).decode().strip()
        expected_tree=git(['rev-parse',case['head']+'^{tree}'],cwd=clone).decode().strip()
        assert imported_tree==expected_tree
        assert git(['diff','--exit-code','--no-ext-diff','--no-textconv'],cwd=clone)==b''
        files=len(git(['ls-files','-z'],cwd=clone).split(b'\0'))-1
        results.append({**case,'imported_tree':imported_tree,'expected_tree':expected_tree,'tree_equal':True,'working_tree_equals_index':True,'tracked_files':files,'base_HEAD_unchanged_no_commit':True})
except Exception as failure:
    failures.append({'kind':type(failure).__name__,'message':str(failure)})
finally:
    after={str(path):snapshot(path) for path in [*source_paths,*original_paths]}
    comparisons=[]
    for path,prior in before.items():
        current=after[path]
        comparisons.append({'path':path,'category':'source_worktree' if Path(path) in source_paths else 'original_workspace','before':prior,'after':current,'unchanged':prior==current})
    cleanup=[]
    for clone in clones:
        assert clone.parent==clone_parent and clone.name in {case['name'] for case in plan['cases']}
        assert not clone.is_symlink()
        if clone.exists(): shutil.rmtree(clone)
        cleanup.append({'path':str(clone),'absent':not os.path.lexists(clone),'only_private_clone_deleted':True})
    assert not any(clone_parent.iterdir())
    clone_parent.rmdir()
    assert not clone_parent.exists()

index=Path(plan['bundle'])/'delivery-index.json'
assert hashlib.sha256(index.read_bytes()).hexdigest()==plan['index_sha256']
passed=not failures and len(results)==4 and all(record['unchanged'] for record in comparisons) and all(record['absent'] for record in cleanup)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_4_EXACT_SOURCE_TREE_IMPORTS' if passed else 'CHANGES_REQUESTED_PORTABILITY','scope':'SOURCE_TREE_PORTABILITY_ONLY_NO_BUSINESS_CERTIFICATION','index_sha256':plan['index_sha256'],'cases':results,'workspace_recheck':comparisons,'clone_cleanup':cleanup,'clone_parent_absent':not clone_parent.exists(),'failures':failures,'commands':commands,'limitations':['This replay checks patch bytes and imported Git trees, not semantics or business runtime.','No own authored control is independently certified by this tree-only replay; prior Fault review remains separate.','Original recheck covers HEAD/branch/all refs and tracked plus untracked nonignored Git-visible changes; ignored files not inspected.','No SDK/API/Docker/Gradle/harness/provider/CI execution; no new commits.'],'business':'NOT_EXECUTED','SDK_API_Docker_Gradle_commits':0}
path=ROOT/'receipt.json'; path.write_text(json.dumps(receipt,indent=2)+'\n'); os.chmod(path,0o600)
print(receipt['status'])
for record in results: print(record['name'],record['imported_tree'],record['tree_equal'])
print('workspaces_unchanged',sum(record['unchanged'] for record in comparisons),'/',len(comparisons))
print('clones_absent',sum(record['absent'] for record in cleanup),'/',len(cleanup))
print('receipt_sha256',hashlib.sha256(path.read_bytes()).hexdigest())
if not passed: raise SystemExit(1)
