"""JO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LoginView


from django.views.defaults import server_error
from .views import vue_de_test
from .views import index
from .views import profile
from .views import registration
from .views import offres

from django.conf import settings
from django.conf.urls import static

from django.contrib.auth import views



    

urlpatterns = [

    path('', index, name = "index"),
    path('utilisateur/', include("utilisateur.urls")),
    path('index.html', index, name = "index2"),
    path('registration.html', registration, name = "registration"),
    path('offres.html', offres, name = "offres"),
    path('accounts/login', LoginView, name='login'),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/profile/', profile),
 #   path('pgadmin4/', views.pgadmin4),
    path('error/',server_error),
    path('test/',vue_de_test)
        ]
