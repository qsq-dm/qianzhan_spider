#!/usr/bin/env bash
cd /home/apps/qianzhan_spider
dt=$(date "+%Y-%m-%d")
path_to_log="log/""$dt""_qianzhan_spider_1000_base_login.log"
echo $path_to_log
python qianzhan_spider_1000_base_login/setup.py &
