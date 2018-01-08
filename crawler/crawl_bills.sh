#!/bin/bash

year=$1

for county in */ ; do
    # ptcc remove councilor name in bills
    if [ $county != "ptcc/" ]; then
        echo "$year $county"
        cd $county
        rm ../../data/$county/bills-$year.json 2> /dev/null && scrapy runspider bills.py -o ../../data/$county/bills-$year.json -s FEED_EXPORT_ENCODING=utf-8 -s LOG_LEVEL=INFO
        cd ../
    fi
done
