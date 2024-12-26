"""
URL configuration for lab6_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path
from api_v1.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product_catalog.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('cart.urls')),
    path('', include('order.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('api_v1.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),

]
