# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q, F
from django.db import connections, IntegrityError, transaction

from standpoints.models import Standpoints, User_Standpoint
from users.models import Achievements


def tag_create_achievement(user):
    levels = [
        {'number': 99, 'name': 'tags_100'},
        {'number': 49, 'name': 'tags_50'},
        {'number': 0, 'name': 'tags_1'}
    ]
    tags_count = sum(Standpoints.objects.filter(user=user).aggregate(Count('bill', distinct=True), Count('vote', distinct=True)).values())
    for level in levels:
        if tags_count > level['number']:
            Achievements.objects.get_or_create(user=user, name=level['name'])
            break
    return

def tag_pro_achievement(standpoint_id):
    levels = [
        {'number': 99, 'name': 'tag_pro_100'},
        {'number': 17, 'name': 'tag_pro_18'},
        {'number': 3, 'name': 'tag_pro_3'}
    ]
    try:
        standpoint = Standpoints.objects.get(uid=standpoint_id)
        for level in levels:
            if standpoint.pro > level['number']:
                Achievements.objects.get_or_create(user=standpoint.user, name=level['name'])
                break
    except:
        return
