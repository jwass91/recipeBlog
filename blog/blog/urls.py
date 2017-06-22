"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from posts import views as posts_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/$', posts_views.posts_list, name="posts"),
    url(r'^$', posts_views.posts_list),
    url(r'^posts/create/$', posts_views.posts_create, name="create"),
    url(r'^posts/detail/(?P<slug>[\w-]+)$', posts_views.posts_detail, name="detail"),
    url(r'^posts/detail/(?P<slug>[\w-]+)/edit/$', posts_views.posts_update, name="update"),
    url(r'^posts/detail/(?P<slug>[\w-]+)/delete/$', posts_views.posts_delete, name="delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # ulpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  