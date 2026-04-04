"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # -------------------------------------------------------
    # API 路由
    # 模块化 Apps — 每个 App 管理自己的 urls.py
    # -------------------------------------------------------
    path('api/users/',      include('users.urls')),
    path('api/monuments/',  include('monuments.urls')),
    path('api/quiz/',       include('quiz.urls')),
    path('api/system/',     include('system.urls')),
    # 新增模块
    path('api/forum/',      include('forum.urls')),
    path('api/cocreation/', include('cocreation.urls')),
    path('api/stamps/',     include('stamps.urls')),

    # DRF 内置 Auth（登录/登出 UI，开发期使用）
    path('api/auth/', include('rest_framework.urls')),
]

# 开发环境下由 Django 自身托管媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

