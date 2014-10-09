#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import argparse, os
import json
from elasticsearch import Elasticsearch

basepath = "/app/councilor-voter-guide/data/pretty_format"
councilors = ['tccc/councilors.json','tcc/councilors.json','ntcc/councilors.json']
eshost = "localhost"
esindex = 'g0v-voter-guide'
estype = 'councilors'

script_dir =os.path.dirname(__file__)
file_mapping = os.path.join(script_dir, 'mapping-councilors.json')

def esimport():
    es = Elasticsearch([{'host': eshost, 'port': 9200}])
    es.indices.create(index=esindex, ignore=400)
    # es.indices.delete_mapping(index=esindex,doc_type=estype)
    mapping = json.load(open(file_mapping ,'r'),encoding="utf-8")
    es.indices.put_mapping(index=esindex,doc_type=estype, body=mapping)
    for cpath in councilors :
        jarr = json.load(open( os.path.join(basepath, cpath) ,'r'),encoding="utf-8")
        for x in jarr:
            try:
                x['id'] = u"%s-%s-%s" % (x['name'],x['county'],x['election_year'])
                # from "district": "石門區、三芝區、淡水區、八里區"
                # to "district": ["石門區",'三芝區","淡水區","八里區"]
                district = x['district']
                x['district']  = district.split(u"、") if u"、" in district else  [district]
                es.index(index=esindex, doc_type=estype, id= x['id'], body=x)
            except ValueError:
                print("Oops! ValueError:")
                print(json.dumps(x, indent=4,ensure_ascii=False,encoding='utf8'))

def main():
    parser = argparse.ArgumentParser(description='make a list.json with sha256(binary)')
    parser.add_argument('-i', '--path', help='Input directory', required=True)
    parser.add_argument('-w', '--hostpath', help='Host path', required=True)
    # args = parser.parse_args()
    # print(args.path)
    esimport()
    # r = makelist(args.path,args.hostpath)
    # print json.dumps(r, ensure_ascii=False, indent=4 , encoding='utf8').encode('utf-8')

if __name__ == '__main__':
    main()
