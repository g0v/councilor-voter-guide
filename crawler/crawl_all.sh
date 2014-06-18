#!/bin/bash
rm -f ../data/*.json     
scrapy crawl taipei_meeting -o ../data/taipei_meeting_minutes-11.json -t json        
scrapy crawl taipei_councilor -o ../data/taipei_councilor-11.json -t json  
