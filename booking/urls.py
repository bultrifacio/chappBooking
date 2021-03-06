from django.urls import path

from . import views

app_name= 'booking'
urlpatterns = [
    path('', views.Search.as_view(), name='search'),
    path('results/', views.results, name='results'),
    path('reserve/<int:room_id>/', views.reserve, name='reserve'),
    path('reservations/', views.reservations, name='reservations'),
    path('detail/<int:booking_id>/', views.detail, name='detail'),
    path('detail/<int:booking_id>/pdf', views.BookingPdf.as_view(), name='bookingPdf'),
    path('error/', views.Error.as_view(), name='error'),
]
