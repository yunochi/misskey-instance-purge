## 1. Misskey Instance user purge tool 

Misskey 에서 특정 인스턴스의 유저와 에모지를 모두 삭제하는 툴입니다. Admin 권한이 있는 API토큰이 필요합니다. 

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

<br><br><br>

## 2. Misskey self-destruct tool

Misskey 의 인스턴스 self-destruct 도구입니다. 내 서버에 있는 모든 계정을 삭제합니다.  인스턴스를 서비스 종료하기 위해서 사용할 수 있습니다.  Admin 권한이 있는 API토큰이 필요합니다.  
  
**주의** : 다른 액티비티펍 서버들로 계정 삭제가 전달되는 것은 전적으로 미스키의 구현에 의존합니다. 또한, 이 툴을 실행한 후 모든 서버들로 계정삭제가 전달될 수 있도록 충분한 시간동안 서버를 켜 놔야 합니다.  


### 사용법

1. config.yaml 설정 파일을 만듭니다. 설정파일은 위 user purge tool 과 호환됩니다. 다만 `targetHost` 설정은 무시됩니다. 
2. 필요한 의존성을 설치합니다.
    ```commandline
    pip install -r requirements.txt
    ```
3. `python self-destruct.py` 로 실행합니다. 
4. root계정 (가장 처음 만들어진 계정) 은 API로 삭제할 수 없습니다. root계정도 삭제해야 하는 경우 DB에서
    ```sql
    UPDATE "user" SET "isRoot" = FALSE WHERE "isRoot" IS TRUE
    ```
    를 사용하여 isRoot를 해제하고 root유저를 삭제합니다. 