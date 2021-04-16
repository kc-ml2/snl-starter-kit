# snl-starter-kit
SNL에 참여 하기위한 stater kit 입니다.

## Prerequisite

* Docker Hub account
   * https://hub.docker.com/
* Docker Engine
    * tested on CentOS, Ubuntu, MacOS
    
## How-To

Directories
```
snl-starter-kit/
  /src
  /submit.sh
```

src 폴더안의 algo에 본인의 에이전트를 구현하시면 됩니다.

* `Agent`라는 이름의 class에 `act`라는 이름의 method는 꼭 정의 되어있어야 합니다.
```python
class Agent:
    def __init__(self):
        pass

    def act(self, obs):
        pass
```

* agent_factory라는 method에 inference(혹은 test) time을 위한 initializing하여 agent instance를 return 해주셔야 합니다.
```python
def agent_factory():
    agent = Agent()

    return agent
```

* 에이전트 제출
```shell
docker login
# log in with your account info

# below script will build and push docker image
sh submit.sh {{dockerhub_username}} {{dockerhub_password}} {{repository(imagename)}} {{tag}}
```
