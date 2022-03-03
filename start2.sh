#bash
echo "Starting DRipper containers..."

 docker-compose down
 docker rm -f $(docker ps --format "{{.ID}}")
 docker image prune --all --force
 git init .
 #git stash
 git pull origin master

  count=$1
  if [ -z "$count" ]; then
   count=5
  fi
  docker-compose up --build -d --scale app=$count

  echo "Sleep 30..."
  sleep 30 # run time

  echo "down..."
  
  docker-compose down
echo "......................END START2.SH.................."
