# -*- coding: utf-8 -*-
from django import forms


class NameForm(forms.Form):
    content = forms.CharField(label=u'文字', widget=forms.widgets.Textarea(attrs={'class': 'form-control'}))
