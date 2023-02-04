# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

import json
def keyword(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword").lower()
        data_files = []

        for root, dirs, files in os.walk("DEPO_DATA"):
            for file in files:
                if file.endswith('.json'):
                    data_files.append(os.path.join(root, file))

        results = []
        for file in data_files:
            with open(file, "r") as f:
                data = json.load(f)

            witness = data['witness']

            
            for i, x in enumerate(data['data']):
                ctx = ""
                if keyword in x['text'].lower():
                    try:
                        ctx += data['data'][i-1]['text']
                    except:
                        pass
                    ctx += x["text"]
                    try:
                        ctx += data['data'][i+1]['text']
                    except:
                        pass
                    context = {
                        "context":ctx,
                        "witness":witness,
                        "page_#":x['page_#'],
                        "url":data['url']+str(x['page_#'])
                        }
                    results.append(context)
            

        return JsonResponse({"status":"success", "results":results, "keyword":keyword})
    else:
        return render(request, "keyword.html")