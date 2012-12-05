from django.conf.urls.defaults import *

#=============================================================================== Patterns
urlpatterns = patterns('buzzer.views',
                       url(r'^getBuzzes[/]?', 'getBuzzes'),
                       url(r'^getBuzz[/]?', 'getBuzz'),
                       url(r'^trebek[/]?', 'trebek'),
                       url(r'^clearBuzzes[/]?', 'clearBuzzes'),
                       url(r'^setStatus[/]?', 'setStatus'),
                       url(r'^board[/]?', 'board'), 
                       url(r'^getStatus[/]?', 'getStatus'),
                       url(r'^players[/]?', 'players'), 
                       url(r'^register[/]?', 'register'),
                       url(r'^buzz[/]?', 'buzz'),
                       url(r'^logout[/]?', 'logout'),
                       (r'', 'player'),
		       )
