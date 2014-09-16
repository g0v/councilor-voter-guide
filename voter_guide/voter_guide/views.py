#-*- coding: UTF-8 -*-
from django.shortcuts import render


def about(request):
    return render(request,'about.html', {})

def reference(request):
    return render(request,'reference.html', {})
