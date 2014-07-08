#!/bin/bash
rm -f ../data/taipei/*.json     
scrapy crawl taipei_meeting -o ../data/taipei/meeting_minutes-11.json -t json        
scrapy crawl taipei_councilor -o ../data/taipei/councilor-11.json -t json  
scrapy crawl taipei_councilor_terms -o ../data/taipei/councilor_1-11.json -t json  
scrapy crawl taipei_bills -o ../data/taipei/bills-11.json -t json
