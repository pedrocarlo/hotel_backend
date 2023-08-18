#!/bin/bash

# echo CHANGED
celery -A hotel_api.tasks worker -l INFO --logfile=./celery/celery_worker.log --detach
# echo "HELLO FROM WORkER"
celery -A hotel_api.tasks beat -l INFO --logfile=./celery/celery_beat.log --detach

