# -*- coding: utf-8 -*-
from django import forms
from .models import Intent

class IntentForm(forms.ModelForm):

    class Meta:
        model = Intent
        fields = ['name', 'county', 'constituency', 'platform']
