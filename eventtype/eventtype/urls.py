"""eventtype URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
import resolver.views
import eventtype.settings

urlpatterns = [
    url(r'^eventtype/admin/', admin.site.urls),
    url(r'^eventtype/$', resolver.views.index),
    url(r'^eventtype/resolve/$', resolver.views.resolve),
    url(r'^eventtype/build/$', resolver.views.builder),
    url(r'^eventtype/about/$', resolver.views.about),
]#  + static(eventtype.settings.STATIC_SUFFIX, document_root=eventtype.settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
