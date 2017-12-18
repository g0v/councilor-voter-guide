# -*- coding: utf-8 -*-
from users.models import Achievements


def intent_register_achievement(user):
    Achievements.objects.get_or_create(user=user, name='intent_register')
    return

def intent_like_achievement(user, exceed_100=False):
    Achievements.objects.get_or_create(user=user, name='intent_liked_1')
    if exceed_100:
        Achievements.objects.get_or_create(user=user, name='intent_liked_100')
    return
