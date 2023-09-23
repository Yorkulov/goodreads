from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from .views import home_page, lending_page

urlpatterns = [
    path('', lending_page, name='lending_page'),
    path('home/', home_page, name='home_page'),

    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('api/', include('api.urls')),

    path('api-auth/', include('rest_framework.urls')),

    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)