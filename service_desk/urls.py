from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from accounts.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('accounts/', include('accounts.urls')),
    path('tickets/', include('tickets.urls')),
    path('departments/', include('departments.urls')),
    path('', RedirectView.as_view(pattern_name='accounts:login', permanent=False), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)