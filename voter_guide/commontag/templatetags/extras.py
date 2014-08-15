# -*- coding: utf-8 -*-
import re
import json
from django.core.serializers.json import DjangoJSONEncoder
from django import template
from django.utils.safestring import mark_safe
from councilors.models import CouncilorsDetail


register = template.Library()

@register.filter(name='distinct_district')
def distinct_district(value, arg):
    return CouncilorsDetail.objects.filter(county=value, election_year=arg).exclude(district='').values_list('district', flat=True).distinct()

@register.filter(name='vote_result')
def vote_result(value, arg):
    attribute = {
        'Passed': {
            'td_bgcolor': u'CCFF99',
            'cht': u'通過'
        },
        'Not Passed': {
            'td_bgcolor': u'FF99CC',
            'cht': u'不通過'
        }
    }
    if attribute.get(value):
        return attribute.get(value).get(arg)

@register.filter(name='election_year_range')
def election_year_range(value):
    election_years = ['1969', '1973', '1977', '1981', '1985', '1989', '1994', '1998', '2002', '2006', '2010', '2014', '2018']
    for i in range(0, len(election_years)):
        if election_years[i] == value:
            return '%s~%s' % (value, election_years[i+1])

@register.filter(name='mod')
def mod(value, arg):
    return value % arg

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='multiply')
def subtract(value, arg):
    return value * arg

@register.filter(name='divide')
def divide(value, arg):
    if arg:
        try:
            return "{0:.2f}".format(100.0 * value / arg)
        except Exception, e:
            print e
    else:
        return 0

@register.filter(name='as_json')
def as_json(data):
    return mark_safe(json.dumps(data, cls=DjangoJSONEncoder))

@register.filter(name='replace')
def replace(value, arg):
    if arg:
        for word in arg.split():
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            value = pattern.sub('<font style="background-color: #FFFF66;">'+word+'</font>', value)
        return value
    else:
        return value
