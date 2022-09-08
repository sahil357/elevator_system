from django.contrib import admin
from .models import Elevator, ElevatorTravelLog

class ElevatorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Elevator, ElevatorAdmin)

class ElevatorTravelLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(ElevatorTravelLog, ElevatorTravelLogAdmin)