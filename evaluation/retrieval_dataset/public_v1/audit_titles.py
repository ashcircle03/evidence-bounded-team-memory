"""Write only verification outcomes from public Mozilla metadata and history."""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from build import prepare


def get(path, params):
    url='https://bugzilla.mozilla.org/rest/'+path+'?'+urlencode(params,doseq=True)
    data=subprocess.check_output(['curl','--retry','2','--max-time','60','-fsSL',url])
    return json.loads(data)['bugs']


def main(raw):
    issues,_,_,ids,_=prepare(raw)
    cache=raw/'audit.json'
    result=json.loads(cache.read_text()) if cache.exists() else {}
    keys=sorted(ids-result.keys(),key=int)
    for pos in range(0,len(keys),25):
        batch=keys[pos:pos+25]
        # permissive mode ignores bugs that have become private.
        current=get('bug',dict(id=','.join(batch),include_fields='id,summary,creation_time',permissive=1))
        active=[str(r['id']) for r in current]
        if not active: continue
        histories=get('bug/'+active[0]+'/history',dict(ids=active[1:]))
        by_id={str(r['id']):r['history'] for r in histories}
        for row in current:
            i=str(row['id'])
            same_time=datetime.fromisoformat(row['creation_time'].replace('Z','+00:00'))==datetime.fromisoformat(issues[i]['Created'])
            if i not in by_id or not same_time or row['summary']!=issues[i]['Summary']:
                result[i]='metadata_mismatch'
            elif any(c['field_name']=='summary' for h in by_id[i] for c in h['changes']):
                result[i]='changed'
            else:
                result[i]='unchanged'
    (raw/'audit.json').write_text(json.dumps(result,sort_keys=True)+'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))
