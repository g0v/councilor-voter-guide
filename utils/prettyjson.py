r"""Command-line tool to validate and pretty-print JSON

Usage::
    $ cd crawler/tccc
    $ scrapy crawl councilors -o /tmp/test.json
    # save to file
    $ python ../../utils/prettyjson.py /tmp/test.json /tmp/pretty.json
    # print to sdtout
    $ python ../../utils/prettyjson.py /tmp/test.json
    # print item[3] by indext
    $ python ../../utils/prettyjson.py /tmp/test.json 3
    
"""
import sys
import json
import io

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def main():
    index = -1
    if len(sys.argv) == 1:
        infile = sys.stdin
        outfile = sys.stdout
    elif len(sys.argv) == 2:
        infile = open(sys.argv[1], 'rb')
        outfile = sys.stdout
    elif len(sys.argv) == 3:
        infile = open(sys.argv[1], 'rb')
        if is_int(sys.argv[2]):
            index = int(sys.argv[2])
            outfile = sys.stdout
        else:
            outfile = io.open(sys.argv[2], 'w', encoding='utf8')
    else:
        raise SystemExit("{0} [infile [outfile/itemindex]]".format(sys.argv[0]))
    try:
        obj = json.load(infile)
        if index >=0 :
            obj = obj[index]
    except ValueError, e:
        raise SystemExit(e)
    jd = json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False, encoding='utf8')
    outfile.write(jd)
    outfile.write(u'\n')

if __name__ == '__main__':
    main()