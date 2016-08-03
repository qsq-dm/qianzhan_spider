#!/usr/bin/env bash
cd /home/apps/qianzhan_spider
dt=$(date "+%Y-%m-%d")
path_to_log="log/""$dt""_run_spider_gaoxin_login.log"
echo $path_to_log
python qianzhan_spider_gaoxin_login/setup.py &
