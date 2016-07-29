#!/usr/bin/env bash
cd /home/apps/qianzhan_spider
dt=$(date "+%Y-%m-%d")
path_to_log="log/""$dt""_crawl_gaoxin.log"
echo $path_to_log
scrapy crawl qianzhan_spider_gaoxin -s LOG_FILE=$path_to_log &
