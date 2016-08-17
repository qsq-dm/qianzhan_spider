#!/usr/bin/env bash
cd /home/apps/qianzhan_spider
dt=$(date "+%Y-%m-%d")
path_to_log="log/""$dt""_run_spider_zhaopin_detail_login.log"
echo $path_to_log
python qianzhan_spider_zhaopin_detail_login/setup.py &
