#!/usr/bin/env python
#coding:UTF-8
import json
import subprocess

#d = {
#    "person_id": "53eafef2cc89eebc09c11cd2",
#    "organization_id": "53ec53086370cbbf3f29db13"
#}

d = {
    "birth": "1963-04-20",
    "constituency": "臺北市第一選區",
    "contact_details": [
        {
            "label": "電子信箱",
            "type": "email",
            "value": "tcc9502@tcc.gov.tw"
        },
        {
            "label": "電話",
            "type": "voice",
            "value": "27297708#6008"
        },
        {
            "label": "電話",
            "type": "voice",
            "value": "27297708#6108"
        },
        {
            "label": "傳真",
            "type": "fax",
            "value": "23459123"
        },
        {
            "label": "通訊處",
            "type": "address",
            "value": "台北市信義區仁愛路4段507號608室"
        },
        {
            "label": "通訊處",
            "type": "address",
            "value": "台北市士林區福國路67號"
        }
    ],
    "county": "臺北市",
    "district": "北投區、士林區",
    "education": [
        "國立台北大學企業管理學系研究所碩士、國立台灣大學法律系學士"
    ],
    "election_year": "2010",
    "experience": [
        "執業律師",
        "現任民進黨中央執行委員",
        "現任民進黨台北市黨部主委",
        "民進黨發言人",
        "台北市文湖線調查專案小組成員",
        "謝長廷北區服務處主任",
        "綠色和平電台主持人",
        "台灣國家山岳協會理事長",
        "中央選舉委員會巡迴監察員",
        "台灣教授協會義務律師",
        "謝長廷告訴代理人",
        "游錫堃告訴代理人",
        "李登輝前總統諮詢律師"
    ],
    "gender": "男",
    "image": "http://www.tcc.gov.tw/../upload/photo/%E8%8E%8A%E7%91%9E%E9%9B%842.jpg",
    "in_office": True,
    "links": [
        {
            "note": "議會個人官網",
            "url": "http://www.tcc.gov.tw/Councilor_Content.aspx?s=1027"
        },
        {
            "note": "個人網站",
            "url": "http://www.facebook.com/lawyer0420"
        }
    ],
    "name": "莊瑞雄",
    "party": "民主進步黨",
    "platform": [
        "一、泛綠唯一一席律師議員，關鍵時刻永不缺席。",
        "二、推廣免費法律諮詢，保障基本人權。",
        "三、嚴厲監督市政，為市民荷包把關。",
        "四、爭取婦女就業機會，減輕家庭負擔。",
        "五、提昇老人生活品質，鼓勵老人社會參與。",
        "六、傾聽弱勢聲音，健全社會福利制度。",
        "七、強化校園安全機制，杜絕霸凌建立無毒校園。",
        "八、市府舉辦活動，禁止動員師生、校護支援充人數。",
        "九、禁止市府強迫員工，從事與職掌無關之業務。",
        "十、催促市府盡快落實政策，開發社子島、關渡平原。",
        "十一、關心士林、天母、石牌商圈規劃，促進地方繁榮。",
        "十二、積極推廣在地文化，提振士林、北投觀光產業。",
        "十三、推動士林、北投老舊社區更新，督促士林公有市場改建案。"
    ],
    "remark": []
}
person = json.dumps(d)
print person
cmd = 'curl --user twly.tw@gmail.com:c3oRZ0am --request POST  --header "Accept: application/json" --header "Content-Type: application/json" --data \'%s\' http://test-tw.popit.mysociety.org/api/v0.1/persons' % person
#cmd = 'curl --user twly.tw@gmail.com:c3oRZ0am --request POST --header "Accept: application/json" --header "Content-Type: application/json" --data \'%s\' http://test-tw.popit.mysociety.org/api/v0.1/memberships/' % person
ret = subprocess.check_output(cmd, shell=True)
print ret
