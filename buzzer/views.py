#from django.template import Context, loader
import simplejson, time
from django.shortcuts import render_to_response
from django.http import HttpResponse
from buzzer.models import Player, Setting, Buzz


## -------------Game Host Views------------
def trebek(request):
    return render_to_response('trebek.html')

def clearBuzzes(request):
    Buzz.objects.all().delete()

    return HttpResponse('Deleted')

def setStatus(request):
    newStatus = request.REQUEST['status']
    try:
        status = Setting.objects.filter(name="status")[0]
    except IndexError:
        status = Setting(name="status")

    status.value = newStatus
    status.save()
    return HttpResponse('')

def getBuzzes(request):
    buzzes = [x.name for x in Buzz.objects.all().order_by('id')]
    return HttpResponse(simplejson.dumps(buzzes))

## -------------Board Views------------
def board(request):
    return render_to_response('board.html')

def players(request):
    playerList = [{'name':player.name, 'score':player.score} for player in Player.objects.all()]
    return HttpResponse(simplejson.dumps(playerList))

def getBuzz(request):
    buzz = False
    while(not buzz):
        try:
            buzz = Buzz.objects.filter(retrieved=False).order_by('id')[0]
            buzz.retrieved = True
            buzz.save()
        except IndexError:
            time.sleep(.1)
    return HttpResponse(simplejson.dumps(buzz.name))

def getStatus(request):
    currentStatus = request.REQUEST['currentStatus']
    newStatus = False
    while not newStatus:
        try:
            newStatus = Setting.objects.filter(name="status")[0].value
            if newStatus == currentStatus:
                newStatus = False
        except IndexError:
            pass
        time.sleep(1)
    return HttpResponse(simplejson.dumps(newStatus))

## -------------Player Views------------
# return the registration page
def player(request):

    data = {'name': '',
            'id': ''}
    if request.session.get('playerID'):
        data['id'] = request.session['playerID']
        data['name'] = request.session['name']
    return render_to_response('player.html', data)
    #return HttpResponse("All your base are belong to us")

# post your player name to register for the game
def register(request):
    # add the person to the list of players
    name = request.REQUEST['name']
    if Player.objects.filter(name=name):
        return HttpResponse(simplejson.dumps({'error': "Someone is already using that name(stop trying to cheat)."}))
    
    player = Player(name=name, score=0)
    player.save()
    request.session['name'] = name
    request.session['playerID'] = player.id
    return HttpResponse(simplejson.dumps({'id':player.id}))

def logout(request):
    player = Player.objects.filter(id=request.REQUEST['id'])
    if player:
        player.delete()
    request.session['name'] = ''
    request.session['playerID'] = ''
    return HttpResponse("All your base are belong to us")

# buzz in with your player name
def buzz(request):
    # register a buzz
    name = request.REQUEST['name']
    if Buzz.objects.filter(name=name):
        return HttpResponse(simplejson.dumps({'error': "You already buzzed in (calm down)."}))

    Buzz(name=name, retrieved=False).save()

    return HttpResponse(simplejson.dumps({'success': "Buzzed"}))

