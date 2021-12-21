# Domino_Fuzzer

- Domato + Template Based Fuzzing 방식을 합친 DOM Fuzzer입니다.

  - Domato : https://github.com/googleprojectzero/domato

- 사용법

  ```
  # step1 - run mutate_server
  python3 Domino_server.py
  
  # step2 - Start Fuzzing
  [Windows10]
  python3 run_fuzz_windows10.py --method (normal or iframe) (or --help)
  
  [Ubuntu]
  python3 run_fuzz_ubuntu.py
  ```
  
- 로그 저장 장소

  - 크래시 로그 : ./log/crash_[날짜 및 시간].log

  - 크래시 html : ./log/crash_[날짜 및 시간].html


- 생성한 템플릿 저장 장소
  - ./Test_Templates
  - 이 디렉토리에 템플릿들을 추가하면 됩니다.
  
- Fuzzing 방식 선택 (ver4 추가)


  - Domato Template Based Fuzzing (기존 방식)

    ```bash
    python3 run_fuzz_[windows10 or ubuntu].py --method normal
    ```

  - **iframe** Domato Template Based Fuzzing (추가된 방식)

    ```bash
    python3 run_fuzz_[windows10 or ubuntu].py --method iframe
    ```

## 패치

### 2021-12-22

- git에 업로드
