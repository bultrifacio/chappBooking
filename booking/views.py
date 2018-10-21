from datetime import datetime
import io
from reportlab.pdfgen import canvas
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, FileResponse
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
                            id_card_text=id,
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

def bookingPdf(request, booking_id):
    reservation = get_object_or_404(Booking, pk=booking_id)
    buffer = io.BytesIO()
    reservation_file = canvas.Canvas(buffer)
    reservation_file.drawString(100, 100, "'Cdigo de reserva: '")
    '''file.drawString(100,100,'Código de reserva: {}'.format(reservation.name_text))
    file.drawString(100,100,'Código de reserva: {}'.format(reservation.surname_text))
    file.drawString(100,100,'Código de reserva: {}'.format(reservation.email))
    file.drawString(100,100,'Código de reserva: {}'.format(reservation.phone_number_text))
    file.drawString(100,100,'Código de reserva: {}'.format(reservation.payment_card_text))'''
    reservation_file.showPage()
    reservation_file.save()
    return FileResponse(buffer, filename='{}.pdf'.format(reservation.code))


def error(request):
    return render(request, 'booking/error.html')
