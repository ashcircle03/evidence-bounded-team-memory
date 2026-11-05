"""Local interactive prototype backed by one resident Aurora GPU model."""
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import shlex
import subprocess
import threading
import time
from .store import Store, digest
from . import timeline as t
from .timeline_cli import process_sources

from .core import answer_question, passages
from .aurora_reader import RemoteReader

def ask(store, question, generate):
    state=t.view(store)
    result=answer_question(list(store.load("sources").values()),question,generate,state["relations"])
    result["created_at"]=datetime.now(timezone.utc).isoformat()
    store.put("workbench_answers",result)
    return result


def serve(args):
    store=Store(args.store);reader=RemoteReader(args.job,store);lock=threading.Lock()
    origin='http://127.0.0.1:'+str(args.port)
    html=Path(__file__).with_name('workbench.html').read_bytes()
    def state():
        value=t.view(store)
        value['answers']=sorted(store.load('workbench_answers').values(),key=lambda x:x['created_at'])
        value['job_id']=args.job;value['model']='Qwen3-8B';value['workspace']=str(store.root)
        processed={r['source_id'] for r in t.receipts(store)}
        value['pending_sources']=[s['id'] for s in value['sources'] if s['id'] not in processed]
        return value
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def send(self,status,data,kind='application/json; charset=utf-8'):
            blob=data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False).encode()
            self.send_response(status);self.send_header('Content-Type',kind)
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Length',str(len(blob)));self.end_headers();self.wfile.write(blob)
        def allowed(self):
            return self.headers.get('Host')=='127.0.0.1:'+str(args.port)
        def do_GET(self):
            if not self.allowed():return self.send(403,{'error':'local host only'})
            if self.path=='/':return self.send(200,html,'text/html; charset=utf-8')
            if self.path=='/api/state':
                with lock:return self.send(200,state())
            return self.send(404,{'error':'not found'})
        def do_POST(self):
            if not self.allowed() or self.headers.get('Origin') not in (None,origin):
                return self.send(403,{'error':'same origin only'})
            if self.headers.get('Content-Type','').split(';')[0]!='application/json':
                return self.send(415,{'error':'JSON required'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=100000:raise ValueError('입력은 100KB 이내로 넣어 주세요.')
                data=json.loads(self.rfile.read(length))
                with lock:
                    if self.path=='/api/ingest':
                        owner=data.get('owner','').strip();text=data.get('text','').strip()
                        if not owner or not text:raise ValueError('작성자와 원문을 입력해 주세요.')
                        envelope=dict(owner=owner,observed_at=datetime.now(timezone.utc).isoformat(),
                            source=dict(speaker=owner,location=data.get('location','').strip() or 'worklog://local/'+digest(text),text=text))
                        process_sources(store,reader,'direct')
                        result=t.ingest(store,envelope,reader,'direct')
                    elif self.path=='/api/ask':
                        question=data.get('question','').strip()
                        if not question:raise ValueError('질문을 입력해 주세요.')
                        if not store.load('sources'):raise ValueError('먼저 원문 기록을 넣어 주세요.')
                        result=ask(store,question,reader)
                    elif self.path=='/api/review':result=t.review(store,data['proposal'],data['actor'],data['choice'])
                    elif self.path=='/api/process':result=process_sources(store,reader,'direct')
                    else:return self.send(404,{'error':'not found'})
                    return self.send(200,dict(result=result,state=state()))
            except (ValueError,TypeError,KeyError,RuntimeError,subprocess.SubprocessError) as exc:
                return self.send(400,dict(error=str(exc)))
    print(origin,flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--job',required=True)
    p.add_argument('--store',default='.workbench/records');p.add_argument('--port',type=int,default=8766)
    serve(p.parse_args())
