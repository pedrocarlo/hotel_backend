#!/bin/bash

celery -A hotel_api.tasks worker -l INFO --logfile=celery_worker.log
echo "HELLO FROM WORkER"
celery -A hotel_api.tasks beat -l INFO --logfile=celery_beat.log
echo "HELLO FROM BEAT"
