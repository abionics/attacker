#bash
#cd attacker

for i in {1..3}; do

 echo "Starting DRipper containers..."

 docker-compose down
 docker rm -f $(docker ps --format "{{.ID}}")
 docker image prune --all --force
 git init .
 git pull origin master

  count=$1
  if [ -z "$count" ]; then
   count=3
  fi
  docker-compose up --build -d --scale app=$count

  echo "Sleep 120..."

  sleep 120 # run time

  echo "down..."
  docker-compose down

  sleep 5
done
