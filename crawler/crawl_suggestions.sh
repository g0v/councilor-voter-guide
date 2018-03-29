#!/bin/bash


for county in */ ; do
    if [ $county != "cec/" ]; then
        echo "$county"
        cd $county
        rm -f ../../data/$county/suggestions.json 2> /dev/null && scrapy runspider suggestions.py -o ../../data/$county/suggestions.json -s FEED_EXPORT_ENCODING=utf-8 -s LOG_LEVEL=INFO
        cd ../
    fi
done
