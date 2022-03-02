#bash
#docker-compose down
#docker rm -f $(docker ps --format "{{.ID}}")
#docker image prune --all
#git pull origin master

echo "Starting DRipper containers..."

for i in {1..3}; do
  count=$1
  if [ -z "$count" ]; then
   count=10
  fi
  docker-compose up --build -d --scale app=$count
  
  echo "Sleep 30..."
  
  sleep 30 # run time
   
  echo "down..."
  docker-compose down
   
   sleep 5
done
