#!/bin/bash


cd /opt/Envs/py3/py3_project

source /opt/Envs/py3/bin/activate

scrapy crawl BCHtokenTopHolder -s LOG_FILE=/opt/Envs/py3/py3_project/logs/BCHtokenTopHolder_`date -d today +"%Y%m%d%H%M"`.log



