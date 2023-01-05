from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return HttpResponse("This is the start of an menu page.")