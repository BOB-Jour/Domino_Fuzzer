import shutil
import os
import random
import subprocess
from domato import generator

class Domino():
    def __init__(self):
        self.Domato_PATH = "./domato/"
        self.Test_Template_PATH = "./Test_Templates/"
        self.log_dir = "./log/"
        self.dir_check()
        
        self.template_data_list = [] # template들의 내용을 리스트로 전부 저장
        self.get_template_data()
        self.Domato = generator.Domato()
        
    def get_template_data(self):
        files = os.listdir(self.Test_Template_PATH)
        for file_name in files:
            # 한글이 있는 경우 인코딩에러가 나서 utf-8로 읽어옵니다.
            with open(self.Test_Template_PATH+file_name, 'r', encoding='utf-8') as fp: 
                self.template_data_list.append(self.js_try_catch(fp.read()))

    def select_template(self):
        select = random.randrange(0, len(self.template_data_list))
        return self.template_data_list[select]

    def js_try_catch(self, tmeplate_data): 
        # init
        result = tmeplate_data.split('\n')
        tmp = tmeplate_data.lower().split('\n')
        front_idx = -1
        back_idx = -1
        script_line = []

        # [아래의 경우들에 대해 try ~ catch 문법 적용]
        # 1. <script> 
        #    ...
        #    </script> 
        #
        # 2. <script> ... </script>
        script_tag_flag = False
        for line_num,line in enumerate(tmp):
            if('<script>' in line):
                front_idx = line_num
                script_line = []

                if(line.strip() != '<script>'):
                    l = result[line_num].lstrip()
                    if ('</script>' in line): # 경우 2
                        result[line_num] = " "*(len(line)-len(l)) + "<script> try { " + l[l.find("<script>")+len("<script>"):l.find("</script>")] + " } catch(e) { } </script>"
                        continue

                script_tag_flag = True
                continue
            elif('</script>' in line): 
                back_idx = line_num
                script_tag_flag = False

                result = result[:front_idx+1] + script_line + result[back_idx:]

                front_idx = -1
                back_idx = -1

            if(script_tag_flag):
                l = line.lstrip()
                if (len(l)):
                    if (';' in l):
                        script_line.append(" "*(len(line)-len(l)) + "try { " + result[line_num].lstrip() + " } catch(e) { }")
                    else:
                        script_line.append(result[line_num])
                else:   
                    script_line.append("")
        
        return '\n'.join(result)

    def domato(self, template_data):
        return self.Domato.generator(template_data)

    def make_test(self, make_file_path='./templates/test.html'): 
        stdout = self.domato(self.select_template())
        if (stdout == -1):
            return 0
        
        if(make_file_path == './templates/test.html'): 
            main_temp_back = '''

<html>
<head>
    
    <!-- Refresh_HTML 
    <meta http-equiv="refresh" content="0"> -->
    RELOAD_HTML
    <script type='text/javascript'>
	setTimeout("location.href='http://127.0.0.1:8080/flag?test'",0);
    </script>
</head>
<body>
</body>
</html>
'''
            result_temp = stdout+main_temp_back 
        else: 
            result_temp = stdout

        with open(make_file_path ,'w', encoding='utf-8') as fp:
            fp.write(result_temp)
        print("[+] Gnerate test.html")

    def dir_check(self):
        if os.path.isdir(self.Test_Template_PATH) != True:
            print("[*] Make Test_Templates directory ")
            os.mkdir(self.Test_Template_PATH)
        
        if os.path.isdir(self.log_dir) != True:
            print("[*] Make log directory ")
            os.mkdir(self.log_dir)

if __name__ == "__main__":
    # test code
    domino = Domino()
    domino.make_test()
    



    