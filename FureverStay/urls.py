from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('LandingPage.urls')),
    path('login/', include('LoginPage.urls')),
    path('register/', include('RegistrationPage.urls')),
    path('dashboard/', include('DashboardPage.urls')),
    path('dashboard/owner/', include('PetOwnerDashboard.urls')),
    path('dashboard/sitter/', include('PetSitterDashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
