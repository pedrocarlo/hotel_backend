#!/bin/bash

celery -A hotel_api.tasks worker -l INFO --detach --logfile=/app/celery_worker.log
celery -A hotel_api.tasks beat -l INFO --detach --logfile=/app/celery_beat.log
