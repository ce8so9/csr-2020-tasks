docker exec -i imghost_web_1 /bin/sh -c "mkdir /dev/shm/uploads; chmod 777 /dev/shm/uploads"
docker exec -i imghost_web_1 /bin/sh -c "echo '<img src=https://bats.science/test.png />' > /dev/shm/uploads/test.htm"

