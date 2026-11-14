"""Build a complete source packet without models, stores or experiment results.

New campaign builders should use source_paths rather than copying flat legacy
module filenames. Frozen historical archives remain immutable.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import tarfile
import time


def source_paths(root):
    root=Path(root)
    deadline=time.monotonic()+10
    paths=[]
    for p in (root/'team_memory').rglob('*'):
        if time.monotonic()>deadline:
            raise TimeoutError('Source-only package inventory exceeded10 seconds')
        if p.is_file() and (p.suffix in ('.py','.json','.md','.txt','.html') or p.name in ('LICENSE','NOTICE')):
            if p.is_symlink():
                raise ValueError('Source packet must not follow symlinks')
            paths.append(p.relative_to(root))
    return sorted(paths)


def build(root, output):
    root=Path(root);output=Path(output)
    names=source_paths(root)
    manifest={str(n):sha256((root/n).read_bytes()).hexdigest() for n in names}
    with output.open('xb') as stream, tarfile.open(fileobj=stream,mode='w:gz') as archive:
        for n in names:archive.add(root/n,arcname=str(n),recursive=False)
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    print(json.dumps(build(args.root,args.output),indent=2))


if __name__=='__main__':main()
