#from django.template import Context, loader
import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse
from buzzer.models import Player, Setting


## -------------Game Host Views------------
def trebek(request):
    return render_to_response('trebek.html')

## -------------Board Views------------
def board(request):
    return render_to_response('board.html')

def players(request):
    playerList = [{'name':player.name, 'score':player.score} for player in Player.objects.all()]
    return HttpResponse(simplejson.dumps(playerList))


## -------------Player Views------------
# return the registration page
def player(request):

    return render_to_response('player.html')
    #return HttpResponse("All your base are belong to us")

# post your player name to register for the game
def register(request):
    # add the person to the list of players
    name = request.REQUEST['name']
    if Player.objects.filter(name=name):
        return HttpResponse(simplejson.dumps({'error': "Someone is already using that name(stop trying to cheat)."}))
    
    player = Player(name=name, score=0)
    player.save()
    return HttpResponse(simplejson.dumps({'id':player.id}))

# buzz in with your player name
def buzz(request):
    # register a buzz
    return HttpResponse("All your base are belong to us")
