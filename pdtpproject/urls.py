from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from allauth.account import views as allauthviews
from app.views import index

urlpatterns = [

	#url(r'^$', allauthviews.login),
    url(r'^$', index),
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^portal-special-admin/', admin.site.urls),
    url(r'^app/',include('app.urls')),
    url(r'^deployments/',include('deployments.urls')),
    url(r'^performance/',include('performance.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
