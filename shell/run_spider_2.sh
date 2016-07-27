#!/usr/bin/env bash
cd /home/apps/qianzhan_spider
dt=$(date "+%Y-%m-%d")
path_to_log="log/""$dt""_crawl_1000.log"
echo $path_to_log
python qianzhan_spider_2/setup.py
