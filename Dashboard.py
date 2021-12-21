import curses
import datetime
import threading

'''
# 간단 사용법
0. 사용할 모니터.py에서 Dashbord.Dashbord()를 선언합니다.
    dashboard = Dashbord.Dashbord()
1. 사용할 모니터.py에서 self.LASTEST_CRASH_TIME, self.DCHECK_COUNT, self.CRSAH_COUNT에 대한 것을 수집 할 수 있는 코드들을 넣어줍니다.    
    self.LASTEST_CRASH_TIME = 크래시가 수집된 시간
    self.CRSAH_COUNT = 크래시 로그 개수
    self.DCHECK_COUNT = dcheck 로그 개수
2. 사용할 모니터.py에서 dashboard.run_dashboard(testcase_path)를 호출합니다.
'''

class Dashboard:
    def __init__(self):
        self.CRSAH_COUNT = 0 
        self.LASTEST_CRASH_TIME = 'None' 
        self.STARTTIME = datetime.datetime.now() 
        self.File_Path = None
        self.DCHECK_COUNT = 0
        self.TESTCASE_COUNT = -1 # watcher 함수 조건문에 의해 시작하자마자 +1이 되어 0으로 시작합니다.
        self.Chrome_COUNT = 0 # 크롬 재실행 횟수
        self.Chrome_PID = -1

    def dashboard(self): 
        begin_x = 0; begin_y = 0
        height = 30; width = 80
        curses.initscr()
        curses.curs_set(0)
        field = curses.newwin(height, width, begin_y, begin_x)

        while(1):
            field.refresh()
            running_time = (datetime.datetime.now() - self.STARTTIME).seconds
            running_time_seconds = running_time % 60
            running_time_minutes = running_time // 60 % 60
            running_time_hours = running_time // 60 // 60 % 24
            running_time = "%d:%d:%d" % (running_time_hours, running_time_minutes, running_time_seconds)

            dashboard_template = '''
#############################################################
                        Dash Board                    
=============================================================
  StartTime     :        %s               
  RunTime       :        %s               
  Crash         :        %d                            
  Lastest Crash  :        %s                          
  Dcheck Failed :        %d                   
  TestCase      :        %d                   
  Chrome Count  :        %d         
  Chrome PID    :        %d                   
#############################################################''' % (self.STARTTIME, running_time, self.CRSAH_COUNT, self.LASTEST_CRASH_TIME, self.DCHECK_COUNT, self.TESTCASE_COUNT, self.Chrome_COUNT, self.Chrome_PID)
            field.addstr(0, 0, dashboard_template) 

    def watcher(self):
        testcase_data = b''
        while(True):
            with open(self.File_Path, 'rb') as fp:
                tmp = fp.read()
            if (testcase_data != tmp) and (tmp != b''):
                self.TESTCASE_COUNT += 1
                testcase_data = tmp

    def run_dashboard(self, file_path):
        self.File_Path = file_path
        dashboard_thread = threading.Thread(target=self.dashboard).start()
        watcher_thread = threading.Thread(target=self.watcher).start()

