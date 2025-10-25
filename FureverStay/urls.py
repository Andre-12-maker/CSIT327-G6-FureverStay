from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('LandingPage.urls')),
    path('login/', include('LoginPage.urls')),
    path('register/', include('RegistrationPage.urls')),
    path('dashboard/', include('DashboardPage.urls')),
]
