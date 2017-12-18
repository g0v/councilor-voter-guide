# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect

from .models import Achievements


def achievements(request):
    medals = [
        {'category': u'候選人', 'name': 'intent_register', 'label': u'笑罵由人', 'description': u'若不出來選，天公伯都不會原諒你'},
        {'category': u'候選人', 'name': 'intent_liked_1', 'label': u'妖受讚', 'description': u'按讚任一可能參選人'},
        {'category': u'候選人', 'name': 'intent_liked_100', 'label': u'西瓜甜了', 'description': u'按讚的可能參選人得到讚數破百'},
        {'category': u'標籤認同度', 'name': 'tag_pro_3', 'label': u'三隻小豬', 'description': u'任一標籤得票破三票'},
        {'category': u'標籤認同度', 'name': 'tag_pro_18', 'label': u'十八同人', 'description': u'任一標籤得票破十八票'},
        {'category': u'標籤認同度', 'name': 'tag_pro_100', 'label': u'一呼百應', 'description': u'任一標籤得票破百'},
        {'category': u'標籤數量', 'name': 'tags_1', 'label': u'做功德人', 'description': u'標註任一提案或表決的標籤'},
        {'category': u'標籤數量', 'name': 'tags_50', 'label': u'你標籤機？', 'description': u'不同提案或表決的標籤五十個'},
        {'category': u'標籤數量', 'name': 'tags_100', 'label': u'你不要這麼專業好不好', 'description': u'不同提案或表決的標籤破百'},
    ]
    achievements = Achievements.objects.filter(user=request.user).values('name', 'checked')
    achievements = {x['name']: {'got': True, 'checked': x['checked']} for x in achievements}
    for medal in medals:
        medal['got'] = achievements.get(medal['name'], {}).get('got', False)
        medal['checked'] = achievements.get(medal['name'], {}).get('checked', False)
    achievements = Achievements.objects.filter(user=request.user, checked=False).update(checked=True)
    return render(request, 'users/achievement.html', {'medals': medals})
