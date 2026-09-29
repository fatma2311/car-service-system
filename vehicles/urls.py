from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('cancel-appointment/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
]