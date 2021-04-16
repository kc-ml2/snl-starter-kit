# snl-starter-kit
SNL에 참여 하기위한 stater kit 입니다.

## Prerequisite

* Docker Hub account
   * https://hub.docker.com/
* Docker Engine
    * tested on CentOS, Ubuntu, MacOS
    
## How-To

```shell
docker login
# log in with your account info

# below script will build and push docker image
sh submit.sh {{dockerhub_username}} {{dockerhub_password}} {{repository(imagename)}} {{tag}}
```
