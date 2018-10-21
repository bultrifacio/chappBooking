from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('results/', views.results, name='results'),
    path('<int:room_id>/', views.booking, name='booking'),
    path('reservations/', views.reservations, name='reservations'),
    path('<int:booking_id>/', views.detail, name='detail'),
]
