# -*- coding: utf-8 -*-
import re
from django.utils import simplejson
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(name='ad_year')
def ad_year(value):
    term_end_year = {0:1969, 1:1973, 2:1977, 3:1981, 4:1985, 5:1989, 6:1994, 7:1998, 8:2002, 9:2006, 10:2010, 11:2014}
    try:
        value = int(value)
        return '%s~%s' % (term_end_year.get(value-1, ''), term_end_year.get(value, ''))
    except Exception, e:
        return ''

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
    return mark_safe(simplejson.dumps(data))

@register.filter(name='replace')
def replace(value, arg):
    if arg:
        for word in arg.split():
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            value = pattern.sub('<font style="background-color: #FFFF66;">'+word+'</font>', value)
        return value
    else:
        return value
