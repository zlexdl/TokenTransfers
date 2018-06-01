#!/usr/bin/bash





cd /opt/Envs/py3/py3_project

source /opt/Envs/py3/bin/activate

scrapy crawl EthSysTopHolder -s LOG_FILE=/opt/Envs/py3/py3_project/logs/EthSysTopHolder_`date -d today +"%Y%m%d%H%M"`.log















