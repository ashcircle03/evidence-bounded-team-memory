import json, os
from pathlib import Path
from hashlib import sha256
os.umask(0o077)
p=Path(os.environ['NLTK_DATA'])
p.mkdir(parents=True,exist_ok=False,mode=0o700)
import nltk
nltk.data.path[:]=[str(p)]
for name in ('stopwords','punkt_tab'):
    assert nltk.download(name,download_dir=str(p),force=True,quiet=True,raise_on_error=True)
from nltk.corpus import stopwords
assert 'the' in stopwords.words('english')
from nltk.tokenize import sent_tokenize
assert len(sent_tokenize('One sentence. Another sentence.'))==2
manifest={str(f.relative_to(p)):sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file()}
Path(__file__).with_name('nltk-manifest.json').write_text(json.dumps(manifest,indent=2))
print('PRIVATE_NLTK_READY',p,flush=True)
