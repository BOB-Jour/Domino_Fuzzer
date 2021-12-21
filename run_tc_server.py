from flask import Flask, render_template, redirect, url_for
import jinja2
import Domino

app = Flask(__name__)

# 새로고침 할 때 템플릿이 변경 되었으면 새로 로드
app.config['TEMPLATES_AUTO_RELOAD'] = True 

@app.after_request
def set_response_headers(r):
    r.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    return r

# monitor
@app.route('/')
def home():
    test_case = 'index.html'
    return render_template(test_case)

@app.route('/test')
def run_test():
    test_case = 'test.html'
    while(1):
        try:
            domino.make_test() # ver3 new code
            return render_template(test_case)
        except jinja2.exceptions.TemplateSyntaxError:  # 500에러났을때 hang걸리는거 방지
            print("Exception!")
            continue

@app.route('/foo')
@app.route('/htmlvar00001')
@app.route('/htmlvar00002')
@app.route('/htmlvar00003')
@app.route('/htmlvar00004')
@app.route('/htmlvar00005')
@app.route('/htmlvar00006')
@app.route('/htmlvar00007')
@app.route('/htmlvar00008')
@app.route('/htmlvar00009')
@app.route('/1')
@app.route('/null')
def totest_redirect():
    print("[!] redirect!")
    return redirect("http://127.0.0.1:8080/test")

def run_server():
    app.run(host="127.0.0.1", port=8080, debug=True) # ver3 new code

def main():
    run_server()
    
if __name__ == '__main__':
    domino = Domino.Domino()
    main()