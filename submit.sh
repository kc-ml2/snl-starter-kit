DOCKERHUB_USERNAME="your username"
PASSWORD="your pass"
REPO="repo"
TAG="tag"


RED='\033[0;31m'
NC='\033[0m'

# check if agent is runnable
# if test.py returns non-zero value, then the rest script won't be executed
test_agent() {
  echo "${RED}[INFO] validating your agent...${NC}"
  python test.py
}

# dockerize agent into image and submit to dockerhub
docker_submit() {
  echo "${RED}[INFO] submitting docker image...${NC}"
  REPOTAG "$DOCKERHUB_USERNAME/$REPO:$TAG"
  docker login --username="$DOCKERHUB_USERNAME" --password="$PASSWORD"

  docker build -t "$REPOTAG" .
  docker push "$REPOTAG"
}

test_agent && docker_submit
