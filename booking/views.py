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
    """
    Display a search form.

    **Template:**

    :template:`booking/search.html`
    """
    return render(request, 'booking/search.html')


def results(request):
    """
    Display the room results in a date range

    **Context**

    ``rooms``
        All the available rooms.

    ``total_days``
        Total days of stay.

    **Template:**

    :template:`booking/results.html`
    """
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
        #Variables for other views
        request.session['total_days'] = total_days
        request.session['from_date'] = from_date
        request.session['to_date'] = to_date
        return render(request, 'booking/results.html', {'rooms' : rooms, 'total_days': total_days})


def reserve(request, room_id):
    """
    Display the reserve form.

    **Context**

    ``room``
        An instance of the selected room.

    **Template:**

    :template:`booking/reserve.html`
    """
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'booking/reserve.html', {'room': room})


def reservations(request):
    """
    Display all the reservations of the user.

    **Context**

    ``reservations``
        All the reservations of the user.

    **Template:**

    :template:`booking/reservations.html`
    """
    user = request.user
    reservations = Booking.objects.filter(user=user)
    if request.method == 'POST':
        try:
            name = request.POST['name']
            surname = request.POST['surname']
            email = request.POST['email']
            credit_card = request.POST['creditCard']
            comment = request.POST['comment']
            phone = request.POST['phone']
            id_card = request.POST['idCard']
            room_id = request.POST['roomId']
            room = get_object_or_404(Room, pk=room_id)
            total_days = request.session.get('total_days')
            from_date=request.session.get('from_date')
            to_date=request.session.get('to_date')
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
                            payment_card_text=credit_card,
                            days_number=total_days,
                            amount_number=amount,
                            from_date=from_date,
                            to_date=to_date,
                            date=date,
                            room=room,
                            user=user)
            reservation.save()
            room.available_date = to_date
            room.save()

    return render(request, 'booking/reservations.html', {'reservations': reservations})


def detail(request, booking_id):
    """
    Display the detail view of a reservation.

    **Context**

    ``reservation``
        The selected reservation.

    **Template:**

    :template:`booking/detail.html`
    """
    reservation = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking/detail.html', {'reservation': reservation})


class BookingPdf(View):
    """
    Generate and display the pdf of one reservation details.

    **Context**

    ``reservation``
        An instance of the selected reservation.

    **Template:**

    :template:`booking/pdf.html`
    """
    def get(self, request, booking_id):
        reservation = get_object_or_404(Booking, pk=booking_id)
        params = {
            'reservation': reservation,
            'request': request
        }
        return Render.render('booking/pdf.html', params)

def error(request):
    """
    Display a error view.

    **Template:**

    :template:`booking/error.html`
    """
    return render(request, 'booking/error.html')
