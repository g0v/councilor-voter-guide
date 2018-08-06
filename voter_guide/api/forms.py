# -*- coding: utf-8 -*-
from django import forms


class NameForm(forms.Form):
    content = forms.CharField(label=u'文字', widget=forms.widgets.Textarea(attrs={'class': 'form-control', 'placeholder': u'範例:\n劉耀仁　陳慈慧　王威中　許家蓓　謝維洲　王閔生\n梁文傑　簡舒培　顏若芳　高嘉瑜　張茂楠　林國成\n江志銘　王世堅　阮昭雄　陳政忠　李建昌　何志偉\n童仲彥　李慶元　陳永德　徐世勲　李彥秀　許淑華\n陳重文　林世宗　陳孋輝　吳志剛　吳碧珠　陳彥伯\n黃珊珊　汪志冰　王欣儀　郭昭巖　王孝維　葉林傳\n顏聖冠　闕枚莎　林亭君　黃向羣　李芳儒　厲耿桂芳\n戴錫欽　李傅中武  秦慧珠　陳錦祥　陳義洲　洪健益\n陳建銘　陳炳甫　應曉薇　王鴻薇　李 新　李慶鋒\n潘懷宗　周柏雅　歐陽龍　鍾小平　徐弘庭　林瑞圖\n吳世正　周威佑'}))
