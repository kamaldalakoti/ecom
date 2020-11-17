"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings

from django.urls import path,include
from django.conf.urls.static import static

from django.contrib.admin import AdminSite
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.utils.translation import ugettext_lazy



AdminSite.site_title = ugettext_lazy('ecom')

AdminSite.site_header = ugettext_lazy('ecom')

AdminSite.index_title = ugettext_lazy('DATA BASE ADMINISTRATION')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('',include('ecom_home.urls',namespace='ecom_home'))

]
urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
    document_root=settings.STATIC_ROOT)
