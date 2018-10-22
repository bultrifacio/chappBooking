from datetime import datetime
import io
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Room, Booking
from .render import Render

def search(request):
    context = {'search_page': 'active'}
    return render(request, 'booking/search.html', context)


def results(request):
    try:
        from_date = request.GET['fromDate']
        to_date = request.GET['toDate']
    except:
        return redirect('error')
    else:
        date_format = '%Y-%m-%d'
        rooms = Room.objects.filter(available_date__range=[from_date, to_date])
        from_date_formatted = datetime.strptime(from_date, date_format )
        to_date_formatted = datetime.strptime(to_date, date_format)
        total_days = (to_date_formatted - from_date_formatted).days
        request.session['total_days'] = total_days
        return render(request, 'booking/results.html', {'rooms' : rooms, 'total_days': total_days})


def reserve(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'booking/reserve.html', {'room': room})


def reservations(request):
    context = {'reservations_page': 'active'}
    user = request.user
    reservations = Booking.objects.filter(user=user)
    if request.method == 'POST':
        try:
            name = request.POST['name']
            surname = request.POST['surname']
            email = request.POST['email']
            creditCard = request.POST['creditCard']
            comment = request.POST['comment']
            phone = request.POST['phone']
            id_card = request.POST['idCard']
            room_id = request.POST['roomId']
            room = get_object_or_404(Room, pk=room_id)
            total_days = request.session.get('total_days')
            room_price = request.POST['roomPrice']
            user = request.user
            date = datetime.now().date()
            amount = total_days * float(room_price)
        except:
            return redirect('booking:error')
        else:
            reservation = Booking(
                            name_text=name,
                            surname_text=surname,
                            id_card_text=id_card,
                            email=email,
                            comment_text=comment,
                            phone_number_text=phone,
                            payment_card_text=creditCard,
                            days_number=total_days,
                            amount_number=amount,
                            date=date,
                            room=room,
                            user=user)
            reservation.save()

    return render(request, 'booking/reservations.html', {'reservations': reservations})


def detail(request, booking_id):
    reservation = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking/detail.html', {'reservation': reservation})


class BookingPdf(View):

    def get(self, request, booking_id):
        reservation = get_object_or_404(Booking, pk=booking_id)
        params = {
            'reservation': reservation,
            'request': request
        }
        return Render.render('booking/pdf.html', params)

def error(request):
    return render(request, 'booking/error.html')
