#from django.template import Context, loader
import simplejson, time
from django.shortcuts import render_to_response
from django.http import HttpResponse
from buzzer.models import Player, Setting, Buzz


## -------------Trebek Views------------
def trebek(request):
    return render_to_response('trebek.html')

def setSetting(request):
    name =  request.REQUEST['name']
    value = request.REQUEST['value']
    try:
        setting = Setting.objects.filter(name=name)[0]
    except IndexError:
        setting = Setting(name=name)

    setting.value = value
    setting.save()
    return HttpResponse('')

def getSettings(request):
    settingDict = {}
    for setting in Setting.objects.all():
        settingDict[setting.name] = setting.value
    return HttpResponse(simplejson.dumps(settingDict))

def clearBuzzes(request):
    Buzz.objects.all().delete()

    return HttpResponse('Deleted')

def getBuzzes(request):
    buzzes = [x.name for x in Buzz.objects.all().order_by('id')]
    return HttpResponse(simplejson.dumps(buzzes))

def updatePlayer(request):
    name = request.REQUEST['name']
    score = request.REQUEST['score'] or 0

    player = Player.objects.filter(name=name)[0]
    player.score = score
    player.save()
    
    return HttpResponse('')

## -------------Board Views------------
def board(request):
    return render_to_response('board.html')

def players(request):
    playerList = [{'name':player.name, 'score':player.score} for player in Player.objects.all()]
    return HttpResponse(simplejson.dumps(playerList))

def getBuzz(request):
    buzz = False
    i = 0
    while(not buzz and i < 50):
        try:
            buzz = Buzz.objects.all().filter(retrieved=False).order_by('id')[0]
            buzz.retrieved = True
            buzz.save()
        except IndexError:
            time.sleep(.1)
            i = i + 1
    if buzz:
        return HttpResponse(simplejson.dumps(buzz.name))
    else:
        return HttpResponse(simplejson.dumps(False))

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

