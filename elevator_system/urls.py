"""elevator_system URL Configuration
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
    #post -> to set elevator request
    #get -> get travel logs of the elevators 
    path('elevator/call', csrf_exempt(views.ElevatorTravel.as_view()), name='elevator call and logs'),
    #to check the current elevator floor and last direction of motion
    path('elevator/<int:id>/current_status', csrf_exempt(views.ElevatorCurrentStatus.as_view()), name='elevator call and logs'),
]