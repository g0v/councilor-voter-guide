# -*- coding: utf-8 -*-
import re
from django.db.models import F
from search.models import Keyword


def keyword_list(category, county=''):
    # category: bills, votes, suggestions
    return list(Keyword.objects.filter(category=category, county=county, valid=True).order_by('-hits').values_list('content', flat=True))

def keyword_been_searched(keyword, category, county=''):
    keyword_obj = Keyword.objects.filter(category=category, county=county, content=keyword)
    if keyword_obj:
        keyword_obj.update(hits=F('hits')+1)
    else:
        k = Keyword(content=keyword, category=category, county=county, valid=True, hits=1)
        k.save()
