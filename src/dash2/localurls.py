from django.conf.urls.defaults import *
from django.conf import settings

import os

STATIC = str(os.path.join(os.path.dirname(__file__), 'media/output/fckeditor').replace('\\','/'))
OTHERS = str(os.path.join(os.path.dirname(__file__), 'media/output').replace('\\','/'))

urlpatterns = patterns('',
		#(r'?(P<hash>.*)$', 'dash2.words.views.index'),
		#(r'^(?P<path>.*)#(?P<hash>.*)', 'dash2.words.views.index'),
		#(r'^#(?P<hash>.*)$', 'dash2.words.views.index'),
		(r'^$', 'dash2.words.views.index'),
		(r'^services/pages/$', 'dash2.words.views.service'),
		(r'^fckeditor/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': STATIC,
             'show_indexes': True}),
		(r'^(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': OTHERS,
             'show_indexes': True}),
)
