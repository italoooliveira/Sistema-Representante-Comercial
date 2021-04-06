from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

urlpatterns = [
    path('', include('representacao.urls')),
    path('api/', include('api.urls')),
    path('auth/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
