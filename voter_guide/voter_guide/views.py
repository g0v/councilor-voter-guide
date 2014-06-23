#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect


def about(request):
    return render(request,'about.html', {})

def reference(request):
        return render(request,'reference.html', {})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login/')
