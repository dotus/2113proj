"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from lululemon.views import CustomLoginView,ChangePasswordView
from lululemon.forms import LoginForm

urlpatterns = [
    path("", include("lululemon.urls")),
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='lululemon/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='lululemon/logout.html'), name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='password_change'),
]
urlpatterns += staticfiles_urlpatterns()

