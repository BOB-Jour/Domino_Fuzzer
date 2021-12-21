# monitor
import subprocess
import os
import time
import datetime
import threading
import shutil
import argparse
import Dashboard

BROWSER_PATH = '~\\Target_Chromium_Path\\chrome.exe'

METHOD = None

URL = "http://127.0.0.1:8080/flag?" 
MODE1 = "--incognito"  # 시크릿 모드
MODE2 = "--no-sandbox" # 샌드박스 비활성화
TIMEOUT = 300 # 5min
p = None
RUN_FLAG = False
def main():
    global RUN_FLAG, DASHBOARD, METHOD, p 
    while(1):
        if RUN_FLAG:
            continue
        RUN_FLAG = True

        cmd = []
        cmd.append(BROWSER_PATH)
        cmd.append(URL)
        cmd.append(MODE1)
        cmd.append(MODE2)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, close_fds=True, shell=True)  
        BROWSER_PID = p.pid
        DASHBOARD.Chrome_PID = BROWSER_PID
        while(p.poll() is None): # p.poll()은 일하고있으면 None을 리턴함. 일을 마치면 0리턴
            line = p.stderr.readline()
            if (b"AddressSanitizer" in line):
                # testcase
                now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                testcase_copy = './log/crash_%s_'+now_time+'.html' 
                shutil.copy2('./templates/test.html', testcase_copy % METHOD)

                # dashboard
                DASHBOARD.CRSAH_COUNT += 1
                DASHBOARD.LASTEST_CRASH_TIME = now_time

                # crash log 
                log_path = './log/crash_%s_'+now_time+'.log'
                with open(log_path % METHOD, "wb") as fp:
                    fp.write(line)
                    for line in p.stderr:
                        fp.write(line)

                #set running flag false.
                subprocess.check_output('taskkill /f /im chrome_asan.exe', shell=True)
                DASHBOARD.Chrome_COUNT += 1
                time.sleep(1)
                RUN_FLAG = False

def argparse_init(): 
    parser = argparse.ArgumentParser(description='Domino Monitor')
    parser.add_argument('--method', '-m', help='METHOD : normal : Template Based Domato Fuzzing, iframe : Template Based Domato iframe Fuzzing', default='normal')
    
    return parser

def set_fuzzing_type(parser):
    global URL, METHOD
    args = parser.parse_args()
    if(args.method == 'normal'):
        URL += 'test'
        METHOD = 'normal'
    elif(args.method == 'iframe'):
        URL += 'iframe_test'
        METHOD = 'iframe'
    else:
        parser.print_help()
        os._exit(1)

if __name__ == '__main__':	
    parser = argparse_init()
    set_fuzzing_type(parser)
    try:
        DASHBOARD = Dashboard.Dashboard()
        watch_testcase_name = None
        if (METHOD == 'normal'):
            watch_testcase_name = 'test.html'
        elif(METHOD == 'iframe'):
            watch_testcase_name = 'iframe_tc.html'
        DASHBOARD.run_dashboard('./templates/'+watch_testcase_name)

        while True:
            browser_run_thread = threading.Thread(target=main)
    
            browser_run_thread.start()
            browser_run_thread.join(TIMEOUT) #set timeout 5분 대기

            if browser_run_thread.is_alive():
                subprocess.check_output('taskkill /f /im chrome_asan.exe', shell=True)
                p.stderr.close()
                p.stdout.close()
                DASHBOARD.Chrome_COUNT += 1 
                print("Restart!")
                time.sleep(1)
                RUN_FLAG = False
    except KeyboardInterrupt:
        os._exit(0)