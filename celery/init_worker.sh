#!/bin/bash

# echo CHANGED
rm ./celery/ultNSU.txt
echo "0" > ultNSU.txt
celery -A hotel_api.tasks worker -l INFO --logfile=./celery/celery_worker.log --detach
# echo "HELLO FROM WORkER"
celery -A hotel_api.tasks beat -l INFO --logfile=./celery/celery_beat.log --detach

