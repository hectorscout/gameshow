from django.conf.urls.defaults import *

#=============================================================================== Patterns
urlpatterns = patterns('buzzer.views',
                       url(r'^trebek[/]?', 'trebek'),
                       url(r'^board[/]?', 'board'), 
                       url(r'^players[/]?', 'players'), 
                       url(r'^register[/]?', 'register'),
                       url(r'^buzz[/]?', 'buzz'),
                       (r'', 'player'),
		       )
