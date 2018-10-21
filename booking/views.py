from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Room, Booking

def search(request):
    context = {'search_page': 'active'}
    return render(request, 'booking/search.html', context)


def results(request):
    try:
        from_date = request.GET['fromDate']
        to_date = request.GET['toDate']
    except:
        return redirect('booking/search.html')
    else:
        date_format = '%Y-%m-%d'
        rooms = Room.objects.filter(available_date__range=[from_date, to_date])
        from_date_formatted = datetime.strptime(from_date, date_format )
        to_date_formatted = datetime.strptime(to_date, date_format)
        total_days = (to_date_formatted - from_date_formatted).days
        return render(request, 'booking/results.html', {'rooms' : rooms, 'total_days': total_days})


def reserve(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'booking/reserve.html')


def reservations(request):
    context = {'reservations_page': 'active'}
    return render(request, 'booking/reservations.html', context)


def detail(request):
    context = {}
    return HttpResponse('Details')
