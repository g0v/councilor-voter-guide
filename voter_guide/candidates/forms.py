# -*- coding: utf-8 -*-
from django import forms
from .models import Intent

counties = ((x, x) for x in ["", "臺北市", "新北市", "桃園市", "基隆市", "宜蘭縣", "新竹縣", "新竹市", "苗栗縣", "臺中市", "彰化縣", "雲林縣", "南投縣", "嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"])

parties = ((x, x) for x in ['', '無黨籍', '中國國民黨', '民主進步黨', '臺灣團結聯盟', '親民黨', '新黨', '人民民主陣線', '綠黨', '樹黨', '無黨團結聯盟', '臺灣第一民族黨', '臺灣建國黨', '臺灣民族黨', '華聲黨', '勞動黨', '中華民主向日葵憲政改革聯盟', '大道人民黨', '人民最大黨', '聯合黨', '臺灣主義黨', '中華統一促進黨', '健保免費連線', '民國黨', '大愛憲改聯盟', '時代力量', '自由臺灣黨', '軍公教聯盟黨', '綠黨社會民主黨聯盟', '信心希望聯盟', '臺灣國民會議', '中華民國臺灣基本法連線', '和平鴿聯盟黨', '臺灣獨立黨', '臺灣工黨', '社會福利黨', '泛盟黨', '正黨', '臺灣未來黨', '中華民國機車黨', '中國生產黨', '勞工黨', '中華台商愛國黨'])

class IntentForm(forms.ModelForm):
    class Meta:
        model = Intent
        fields = ['name', 'county', 'constituency', 'party', 'motivation', 'platform', 'experience', 'education', 'remark']
        widgets = {
            'name': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'county': forms.widgets.Select(choices=counties, attrs={'class': 'form-control'}),
            'constituency': forms.widgets.Select(attrs={'class': 'form-control'}),
            'party': forms.widgets.Select(choices=parties, attrs={'class': 'form-control'}),
        }
