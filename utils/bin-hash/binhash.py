#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import logging
import sys, argparse, os
from hashlib import sha256
from datetime import datetime
import json

def makelist(dir,hostpath):
    rlist = []
    r = {'list':rlist, 'created_time': str(datetime.now()) , 'host_path' : hostpath}
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            fpath = os.path.join(subdir, file)
            v = {'name':file, 'dir':subdir, 'sha256': sha256(open(fpath, 'rb').read()).hexdigest(), 'size': os.stat(fpath).st_size}
            rlist.append(v)
    return r

def main():
    parser = argparse.ArgumentParser(description='make a list.json with sha256(binary)')
    parser.add_argument('-i', '--path', help='Input directory', required=True)
    parser.add_argument('-w', '--hostpath', help='Host path', required=True)
    args = parser.parse_args()
    r = makelist(args.path,args.hostpath)
    print json.dumps(r, ensure_ascii=False, indent=4 , encoding='utf8').encode('utf-8')
   
if __name__ == '__main__':
    main()
