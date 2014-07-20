# -*- coding: utf-8 -*-
import subprocess


for i in range(9867, 22759):
    cmd = 'wget -c -O %s.pdf http://sunshine.cy.gov.tw/GipOpenWeb/wSite/SpecialPublication/fileDownload.jsp?id=%s' % (i, i)
    retcode = subprocess.call(cmd, shell=True)
