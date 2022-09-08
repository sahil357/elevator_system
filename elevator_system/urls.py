"""elevator_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #to access data from admin
    path('admin/', admin.site.urls),
    #to add new elevator 
    path('elevator/add', csrf_exempt(views.AddElevator.as_view()), name='add elevator'),
    #to check if the elevator is working or not 
    #also can change the working status of any elevator
    path('elevator/<int:id>/status', csrf_exempt(views.ElevatorStatus.as_view()), name='elevator status'),
    #to check the door status of the elevator
    path('elevator/<int:id>/door_status', csrf_exempt(views.ElevatorDoorStatus.as_view()), name='elevator door status'),
    #to change the door status of the elevator (which will stay like for for 30 secs)
    path('elevator/<int:id>/door_status/<str:door_status>', csrf_exempt(views.ElevatorDoorStatus.as_view()), name='update elevator door status'),
    #
    path('elevator/call', csrf_exempt(views.ElevatorTravel.as_view()), name='elevator call and logs'),
    #to check the current elevator floor and last direction of motion
    path('elevator/<int:id>/current_status', csrf_exempt(views.ElevatorCurrentStatus.as_view()), name='elevator call and logs'),
]