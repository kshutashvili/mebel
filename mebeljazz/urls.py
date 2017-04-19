"""mebeljazz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from mebeljazz.app import application


urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^articles/', include('articles.urls', namespace='articles')),
    url(r'^sitereviews/', include('site_reviews.urls', namespace='site_reviews')),
    url(r'', include(application.urls)),
    url(r'', include('apps.promotions.urls')),
    url(r'', include('common.urls', namespace='common')),
    url(r'^basket/',include('apps.order.urls', namespace='order')),
    url(r'^favlist/$', TemplateView.as_view(template_name='favlist/favlist.html'), name='full_favlist'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
