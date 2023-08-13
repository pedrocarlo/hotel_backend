#!/bin/bash

# docker volume create backend_xml
# docker start dummy
# docker run -d --rm --name dummy -v backend_xml:/app/xml alpine bash
docker cp ./xml backend:/app
# docker stop dummy