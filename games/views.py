import operator
from functools import reduce
from django.http import HttpResponse,JsonResponse
import json
import datetime
import requests
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Category, Game, RegisterUser, RecentlyPlayed
from django.shortcuts import get_object_or_404
from openpyxl import load_workbook
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import random
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    if request.session.get('number'):
        user = RegisterUser.objects.get(number=request.session['number'])
        recent = RecentlyPlayed.objects.select_related('user','game').filter(user=user).order_by("-timestamp_updated").all()[:10]
        most = RecentlyPlayed.objects.select_related('user','game').filter(user=user).order_by("-count").all()[:10]
        return render(request, "games/index.html", {"recent": recent,"most":most})
    else:
        return render(request, "games/index.html")


def games_list(request, cat_slug):
    cat = get_object_or_404(Category, slug__iexact=cat_slug)
    game_list = cat.game_set.order_by('name')
    page = request.GET.get('page', 1)

    paginator = Paginator(game_list, 12, request=request)
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        games = paginator.page(1)
    except EmptyPage:
        games = paginator.page(paginator.num_pages)
    return render(request, 'games/single-game.html', {'games': games, 'cat': cat})


def game_search(request):
    # result = Game.objects.all()
    query = request.GET.get('q')
    # query_list = query.split()
    page = request.GET.get('page', 1)
    # result = Game.objects.filter(
    #        reduce(operator.and_,
    #               (Game(name__icontains=q) for q in query_list))
    #     )
    result = Game.objects.filter(name__icontains=query)

    paginator = Paginator(result, 12)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return render(request, 'games/single-game.html', {'games': result, 'q': query})

def games_list_api(request, cat_slug):
    cat = get_object_or_404(Category, slug__iexact=cat_slug)
    game_list = cat.game_set.order_by('name')
    page = request.GET.get('page', 1)

    paginator = Paginator(game_list.values(), 12)
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        games = paginator.page(1)
    except EmptyPage:
        games = paginator.page(paginator.num_pages)
    # print(dir(games))

    data = {
        'previous_page': games.has_previous() and games.previous_page_number() or None,
        'next_page': games.has_next() and games.next_page_number() or None,
        'games': list(games.object_list)
    }
    return JsonResponse(data)

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        if request.session['otp'] == int(request.POST['otp']):
            del request.session['otp']
            request.session['number'] = request.POST['number']
            number, _ = RegisterUser.objects.get_or_create(number=request.POST['number'])
            dic = {'status':'OK'}
            return JsonResponse(dic)
        else:
            dic = {'status':'NOK'}
            return JsonResponse(dic)

    elif request.method == 'GET':
        key = "45CF5F7D2B3E4E"
        number = request.GET['number']
        otp = random.randint(10**5,10**6-1)
        request.session['otp'] = otp
        msg = "Dear Customer,your OTP for registration is "+str(otp)+"."
        url = "http://login.easywaysms.com/app/smsapi/index.php?key="+key+"&campaign=0&routeid=7&type=text&contacts="+number+"&senderid=CARSWR&msg="+msg
        response = requests.get(url)

        dic = {
            'status_code': response.status_code,
            'reason': response.reason,
            'text': response.text,
            'url': response.url,
            'status':'OK'
        }
        return JsonResponse(dic)

@csrf_exempt
def recentPlayed(request):
    user = RegisterUser.objects.get(number=request.session['number'])
    game = Game.objects.get(name=request.GET['name'])
    try:
        recent, _ = RecentlyPlayed.objects.get_or_create(user=user, game=game)
        recent.timestamp_updated = datetime.datetime.now()
        recent.count = recent.count + 1
        recent.save()
    except Exception as msg:
        print(msg)
    res = []
    res['status'] = "OK"
    res["games"] = recent
    return JsonResponse(res)