## misskey Instance user purge tool 

Misskey 에서 특정 인스턴스의 유저를 모두 삭제하는 툴입니다. Admin 권한이 있는 API토큰이 필요합니다. 

### 사용법 

1. 설정 예제 파일을 config.yaml 으로 복사 합니다. 
    ```commandline
    cp config_example.yaml config.yaml
    ```
2. pyyaml 과 requests 를 설치합니다.
    ```commandline
    pip install -r requirements.txt
    ```
3. 설정 파일을 적절히 편집 후, `python purge.py` 로 실행합니다. 


