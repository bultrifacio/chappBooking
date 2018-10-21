from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def search(request):
    context = {'search_page': 'active'}
    return render(request, 'booking/search.html', context)

def results(request):
    context = {}
    return HttpResponse('Results')


def booking(request):
    context = {}
    return HttpResponse('Booking')


def reservations(request):
    context = {'reservations_page': 'active'}
    return render(request, 'booking/reservations.html', context)


def detail(request):
    context = {}
    return HttpResponse('Details')
