"""Exercise real httpcore transport to catch reserved extension collisions."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import importlib.util
import unittest


@unittest.skipUnless(importlib.util.find_spec('httpx'), 'optional HTTP client')
class TransportTests(unittest.TestCase):
    def test_request_metadata_survives_real_local_http(self):
        import httpx
        from evaluation.reference_qa.contextual.run import TRACE_KEY
        from evaluation.service_v3.dev import TRACE_KEY as DEV_KEY
        from evaluation.service_v3.final import TRACE_KEY as FINAL_KEY
        self.assertEqual(DEV_KEY, FINAL_KEY)
        self.assertNotEqual(DEV_KEY, 'trace')
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'ok')
            def log_message(self, *args):
                pass
        server = HTTPServer(('127.0.0.1',0), Handler)
        thread = Thread(target=server.serve_forever,daemon=True)
        thread.start()
        received = []
        def request_hook(request):
            request.extensions[TRACE_KEY] = {'id':7}
            request.extensions[DEV_KEY] = {'id':8}
        def response_hook(response):
            received.append((response.request.extensions[TRACE_KEY], response.request.extensions[DEV_KEY]))
        try:
            with httpx.Client(trust_env=False, event_hooks={
                    'request':[request_hook], 'response':[response_hook]}) as client:
                response = client.get(f'http://127.0.0.1:{server.server_port}')
                self.assertEqual(response.text,'ok')
                self.assertEqual(received,[({'id':7}, {'id':8})])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
