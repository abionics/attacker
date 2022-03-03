#bash
docker-compose down
docker rm -f $(docker ps --format "{{.ID}}")
git init .
docker image prune --all
git pull origin master

count=$1
if [ -z "$count" ]; then
  count=10
fi
docker-compose up --build -d --scale app=$count
