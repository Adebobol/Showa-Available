from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('Users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
    path("", include('Restaurants.urls')),
    path("", include('cart.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
