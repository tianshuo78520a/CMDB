"""CMDB_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from app01 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('logout/', views.logout),
    path('passwd/', views.passwd),
    path('index/', views.index),

    # 服务
    path('service/', views.service),
    re_path('service/add', views.service_add),
    re_path('service/edit/(\d+)', views.service_edit),
    re_path('service/delete/(\d+)', views.service_delete),
    re_path('service/(\d+)', views.service_info),

    # 用户
    path('user/', views.user),
    path('user_info/', views.user_info),
    re_path('user/add', views.user_add),
    re_path('user/delete/(\d+)', views.user_delete),
    re_path('user_info/add', views.user_info_add),
    re_path('user_info/edit/(\d+)', views.user_info_edit),

    # 机器
    re_path('server/add/', views.server_add),
    re_path('server/edit/(\d+)', views.server_edit),
    re_path('server/delete/(\d+)', views.server_delete),
]
