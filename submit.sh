echo "enter snl email account: "
read ACCOUNT


echo "enter snl upload key: "
read UPLOAD_KEY

echo "enter agent name: (lowercase)"
read AGENT_NAME

echo "optional) enter agent tag: (lowercase)"
read AGENT_TAG

if [[ "$AGENT_NAME" =~ [[:upper:]] ]]; then
  echo "agent name must be lowercase"
  exit
fi

if [ -z "$AGENT_NAME" ]
then
  echo "entered agent name please"
  exit
fi

if [ -z "$AGENT_TAG" ]
then
  AGENT_TAG="latest"
fi

RED='\033[0;31m'
NC='\033[0m'

type curl >/dev/null 2>&1 || { echo >&2 "Required curl but it's not installed. Aborting."; exit 1; }
echo
PAYLOAD='{"email": "'$ACCOUNT'", "upload_key": "'$UPLOAD_KEY'", "name": "'$AGENT_NAME'", "tag": "'$AGENT_TAG'"}'
#PAYLOAD='{"email": "'$ACCOUNT'", "upload_key": "'$UPLOAD_KEY'", "name": "'$AGENT_NAME'""}'


VERIFY_URL="http://211.119.91.202:9990/auth/verify"
COMPLETE_URL="http://211.119.91.202:9990/agents/upload"

response=$(curl -s -w "%{http_code}" -X POST -d "${PAYLOAD}" --header "Content-Type:application/json" $VERIFY_URL)
http_code=$(tail -n1 <<< "$response")  # get the last line

# check if agent is runnable
# if test.py returns non-zero value, then the rest script won't be executed
test_agent() {
  echo "${RED}[INFO] validating your agent... might take a while...${NC}"
  pytest support/tests.py -s
}

# dockerize agent into image and submit to dockerhub
docker_submit() {
  echo "${RED}[INFO] submitting docker image...${NC}"
  REPOTAG="registry.kc-ml2.com/$AGENT_NAME:$AGENT_TAG"
  docker build -t "$REPOTAG" .
  docker push "$REPOTAG"
  curl -s -X POST -d "${PAYLOAD}" --header "Content-Type:application/json" $COMPLETE_URL
  echo "Thanks"
}

if [ "$http_code" == 200 ]; then
  test_agent && docker_submit
else
  echo "check email account or upload key"
fi