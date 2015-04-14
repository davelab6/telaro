# Create your views here.

from jsonrpc import *
from dash2.words.models import Page 
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext, Template
from django.http import HttpResponseRedirect, HttpResponse
from telaro import Text
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

def check_all_letters_in(letters, word):
    for w in word:
        if w.lower() not in letters and w.upper() not in letters:
            return False
    return True

@jsonremote(service)
def getwords (request, selector):

    words_file = "/usr/share/dict/words"

    words = {}
    for w in open(words_file).readlines():
        w = w.strip()
        if w and check_all_letters_in(selector, w):
            words[w.lower()] = 1

    words = words.keys()
    words.sort()
    return words

@jsonremote(service)
def getrandomsentence(response, words):
    calc = Text()
    return calc.run(words)

