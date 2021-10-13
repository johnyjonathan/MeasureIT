"""measureIT URL Configuration

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
from django.urls import path
from measureITapp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('loggedin/', views.loggedin, name="loggedin"),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('createlab/', views.createLab, name="createlab"),
    path('joinlab/', views.joinLab, name="joinlab"),
    path('joinlab/<str:id_number>/', views.LabAuth, name="labauth"),
    path('lab/<str:id_number>/', views.labSite, name="labsite"),
    path('lab/<str:id_number>/add_device', views.addDevice, name="adddevice"),
    path('lab/<str:id_number>/add_man_measure', views.addManualMeasure, name="add_m_measure"),
    path('lab/<str:id_number>/<str:name>', views.device, name="device"),
    path('lab/<str:id_number>/<str:name>/measure_result/<str:command>', views.measureResult, name="measure_result"),
    path('lab/<str:id_number>/list/measures', views.measures, name="measures")

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)