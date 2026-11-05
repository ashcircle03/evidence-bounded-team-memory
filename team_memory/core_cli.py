"""JSON in, JSON out. Model transport is separate from the pure core functions."""
import argparse
import json
from pathlib import Path
import sys
from .core import answer_question,compare_records
from .aurora_reader import RemoteReader
from .store import Store


def main():
    p=argparse.ArgumentParser();p.add_argument('--job',required=True);p.add_argument('--input',default='-')
    p.add_argument('--audit-dir',default='.workbench/core-calls');args=p.parse_args()
    request=json.loads(sys.stdin.read() if args.input=='-' else Path(args.input).read_text())
    generate=RemoteReader(args.job,Store(args.audit_dir))
    if request['operation']=='qa':
        result=answer_question(request['records'],request['question'],generate,request.get('relations',[]))
    elif request['operation']=='compare':result=compare_records(request['earlier'],request['incoming'],generate)
    else:raise ValueError('operation must be qa or compare')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
