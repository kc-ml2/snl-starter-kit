# snl-starter-kit
SNL에 참여 하기위한 stater kit 입니다.

## Prerequisite

* Docker Hub account
   * https://hub.docker.com/
* Docker Engine
    * tested on CentOS, Ubuntu, MacOS
    
## How-To

패키지 설치
```
pip install -r requirements.txt
```

Directories
```
snl-starter-kit/
  /src
  /submit.sh
```

src 폴더안의 algo에 본인의 에이전트를 구현하시면 됩니다.

* `Agent` class에 `act` method는 꼭 정의 되어있어야 합니다.
*  `Agent.act` 메소드의 인자로 환경의 observation이 들어옵니다. observation의 디테일은 comment 혹은 https://github.com/kc-ml2/marlenv를 참조 부탁드립니다.  
```python
class Agent:
    def __init__(self):
        pass

    def act(self, obs):
        pass
```

* Inference(혹은 test) time을 위한 파라미터로 초기화된 agent instance를, `agent_factory` 메소드에서 return 해주셔야 합니다.
* 예를 들어, Epsilon greedy exploration을 하는 agent의 경우, test time에서는 exploration을 원치 않을때, explore=False
```python
def agent_factory():
    agent = Agent(**kwargs_for_inference)

    return agent
```

* 에이전트 제출
```shell
# log in with your account info
docker login


# below script will build and push docker image
sh submit.sh
```

## Notes
### 도커
용량 부족
* 도커 엔진은 사용할 수 있는 저장공간이 제한 되어있습니다. 이미 엔진에 너무 많은 이미지가 있거나, 생성하셨을 경우, 불필요한 이미지를 정리해주시고, `docker system prune`실행 해주세요.

메모리 부족
* 도커 엔진은 사용할 수 있는 메모리공간이 제한 되어있습니다. 이미지를 build 할 때, 간혹 메모리가 부족하다고 뜰 경우, 도커 엔진이 사용 할 수 있는 메모리를 늘려 주시기 바랍니다.

