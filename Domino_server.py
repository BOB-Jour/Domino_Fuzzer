from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse
import Domino
import random


class DominoHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path=urlparse(self.path)
        if(parsed_path.path == "/flag"):
            self.flag(parsed_path.query)
        elif(parsed_path.path == "/test"):
            self.run_test()
        elif(parsed_path.path == "/"):
            self.home()
        elif(parsed_path.path == "/iframe_test"):
            self.run_iframe_test()
        elif(parsed_path.path == "/iframe_tc.html"):
            self.run_iframe_test2()
        return None

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()

    def run_iframe_test(self):
        global DUP_FLAG
        global domino
        global iframe_main_template
        if (DUP_FLAG):
            return None
        else:
            DUP_FLAG = True       

        test_case = 'iframe_tc.html'
        domino.make_test('./templates/'+test_case) 

        width = random.randrange(1,1000)
        height = random.randrange(1,1000)
        msec = random.randrange(50,100)
        html_code = iframe_main_template % (width, height, msec) 

        self._set_response()
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self.wfile.write(bytes(html_code, 'utf-8'))

        return None

    def run_iframe_test2(self): 
        test_case = 'iframe_tc.html'
        with open('./templates/'+test_case, 'rb') as fp:
            html_code = fp.read()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self.wfile.write(html_code)
        return None

    def run_test(self):
        global DUP_FLAG
        global domino
        if (DUP_FLAG):
            return None
        else:
            DUP_FLAG = True       

        test_case = 'test.html'
        domino.make_test() 
        with open ('./templates/'+test_case, 'rb') as fp:
            html_code = fp.read()

        self._set_response()
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self.wfile.write(html_code)
        return None
    
    def flag(self, _redirect):
        global DUP_FLAG
        DUP_FLAG = False
        self.send_response(302) # redirect code 302
        self.send_header('Location', "http://127.0.0.1:8080/"+_redirect)
        self.end_headers()
        return None

    def home(self):
        test_case = 'index.html'
        with open ('./templates/'+test_case, 'rb') as fp:
            html_code = fp.read()
        self._set_response()
        self.wfile.write(html_code)
        return None

def usage(): 
    print("[+] Template Based Domato Fuzzing : http://localhost:8080/flag?test")
    print("[+] Template Based Domato Iframe Fuzzing : http://localhost:8080/flag?iframe_test")

def run(server_class=HTTPServer, handler_class=DominoHTTPHandler, port=8080):
    logging.basicConfig(level=logging.ERROR)
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('[*] Start TestCase Server')
    print('[+] Server Info : http://localhost:8080/')
    usage()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping TestCase Server\n')

if __name__ == '__main__':
    DUP_FLAG = False
    domino = Domino.Domino()
    with open ('./templates/iframe_test.html', 'rt', encoding="utf-8") as fp:
        iframe_main_template = fp.read()
    run()