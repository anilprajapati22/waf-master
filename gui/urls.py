from django.urls import path

from . import views

urlpatterns = [
    path('sgn', views.sgn, name='sgn'),
    path('', views.dockerRun, name='dockerRun'),
    path('<str:container_id>/', views.containerDetails, name='containerDetails'),
    path('<str:container_id>/containerRemove', views.containerRemove, name='containerRemove'),
    path('<str:service_id>/serviceRemove', views.serviceRemove, name='serviceRemove'),
    path('containerList', views.containerList, name='containerList'),
    path('serviceList', views.serviceList, name='serviceList'),
    path('serviceScale', views.serviceScale, name='serviceScale'),
    path('pullimages', views.pullimages, name='pullimages'),    
    #path('', views.index, name='index'),
]