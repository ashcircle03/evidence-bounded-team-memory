import os, tarfile
from pathlib import Path
os.umask(0o077)
folder=Path(__file__).resolve().parent
root=Path(os.environ['NLTK_DATA']); root.mkdir(parents=True,exist_ok=False,mode=0o700)
with tarfile.open(folder/'nltk-data.tar.gz') as archive:
    for member in archive.getmembers():
        rel=Path(member.name)
        assert member.isfile() and not rel.is_absolute() and '..' not in rel.parts
        dest=root/rel; dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(archive.extractfile(member).read())
import nltk
nltk.data.path[:]=[str(root)]
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
assert len(sent_tokenize('One sentence. Another sentence.'))==2
assert 'the' in stopwords.words('english')
print('OFFLINE_NLTK_READY', root, flush=True)
