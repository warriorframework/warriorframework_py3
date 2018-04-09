# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
# Create your views here.
from django.views import View
import requests


class WappStoreView(View):

    template = 'wappstore/wappstore.html'

    def get(self, request):
        """
        Get Request Method
        """
        response = json.loads(requests.get('http://localhost:5000/wapps/get_all_wapps_data/').content)
        return render(request, WappStoreView.template, response)


def expand_wapp(request):
    response = json.loads(requests.get('http://localhost:5000/wapps/get_wapp_info/').content)
    return render(request, 'wappstore/expand_wapp.html', response)