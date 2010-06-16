# Create your views here.

from jsonrpc import *
from dash2.words.models import Page 
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext, Template
from django.http import HttpResponseRedirect, HttpResponse
import urllib

service = JSONRPCService()

def index(request, path=None):
    args = {'title': '',
            'noscript': '', 
            }
    context_instance=RequestContext(request)
    context_instance.autoescape=False
    return render_to_response('index.html', args, context_instance)

@jsonremote(service)
def getPage (request, num):
	return json_convert([Page.objects.get(id=num)])

@jsonremote(service)
def getPageByName (request, name):
	return json_convert([Page.objects.get(name=name)])

@jsonremote(service)
def getPages (request):
	return json_convert(Page.objects.all())

@jsonremote(service)
def updatePage (request, item):
	t = Page.objects.get(id=item['id'])
	t.name = item['name']
	t.text = item['text']
	t.save()
	return getPages(request)

@jsonremote(service)
def addPage (request, item):
	t = Page()
	t.name = item['name']
	t.text = item['text']
	t.save()
	return getPages(request)

@jsonremote(service)
def deletePage (request, num):
	t = Page.objects.get(id=num)
	t.delete()
	return getPages(request)

