# -*- coding: utf-8 -*-
from django import forms
from .models import Platforms

counties = ((x, x) for x in ["全台", "臺北市", "新北市", "桃園市", "基隆市", "宜蘭縣", "新竹縣", "新竹市", "苗栗縣", "臺中市", "彰化縣", "雲林縣", "南投縣", "嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"])

class PlatformsForm(forms.ModelForm):
    class Meta:
        model = Platforms
        fields = ['county', 'content']
        widgets = {
            'county': forms.widgets.Select(choices=counties, attrs={'class': 'form-control'}),
        }
