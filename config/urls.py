from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from vehicles import views as vehicle_views

urlpatterns = [
    path('', vehicle_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='vehicles/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/', include('accounts.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('assistant/', include('ai_agent.urls')),
]

