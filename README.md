# snl-starter-kit
SNL에 참여 하기위한 stater kit 입니다.

## Prerequisite

* Docker Engine
    * tested on CentOS, Ubuntu, MacOS
    
## How-To

```shell
# below script will build and push docker image
sh submit.sh {{dockerhub_username}} {{dockerhub_password}} {{repository(imagename)}} {{tag}}
```