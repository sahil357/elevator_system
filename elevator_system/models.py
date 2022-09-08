from django.db import models

STATUS = (
    (1, "Working"),
    (2, "In Maintenance"),
    (3, "Not Working"),
)

DOOR_STATUS = (
    (1, "open"),
    (2, "close")
)

TRAVEL_DIRECTION = (
    (1, "Up"),
    (2, "Down"),
    # (3, "Same")
)

REQUESTION_OPTIONS = (
    (1, "Outside"),
    (2, "Inside")
)

REQUESTION_STATUS_OPTIONS = (
    (1, "Success"),
    (2, "Failure"),
    #(3, "Inprogess")
)

FAILURE_REASON = (
    (1, "None of the Elevators in available"),
    (2, "All Working Elevators are stuck on some other floor, please try after some time"),
    (3, "Invalid request"),
)

class Elevator(models.Model):
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
    floor = models.PositiveSmallIntegerField(default = 0)
    last_travel_direction = models.PositiveSmallIntegerField(choices=TRAVEL_DIRECTION, default=3)
    # door_status = models.PositiveSmallIntegerField(choices=DOOR_STATUS, default=1)

    def __str__(self):
        return 'Elevator ' + str(self.id)
    
    def get_status(self):
        return dict(STATUS).get(self.status)
    
    def get_last_travel_direction(self):
        return dict(TRAVEL_DIRECTION).get(self.last_travel_direction)
    
class ElevatorTravelLog(models.Model):
    elevator_id = models.ForeignKey(Elevator, on_delete = models.SET_NULL, null=True)
    # user_id = models.ForeignKey(User, on_delete = models.CASCADE )
    request_from = models.PositiveSmallIntegerField(choices = REQUESTION_OPTIONS, default = 1)
    request_status = models.PositiveSmallIntegerField(choices = REQUESTION_STATUS_OPTIONS, default = 1)
    request_door = models.PositiveSmallIntegerField(choices = DOOR_STATUS, default = None, null = True)
    failure_reason = models.PositiveSmallIntegerField(choices = FAILURE_REASON, default = None, null = True)
    floor_from = models.PositiveSmallIntegerField(default = None, null = True)
    floor_to = models.PositiveSmallIntegerField(default = None, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Travel details of Elevator' + str(elevator_id)

    def get_request_from(self):
        return dict(REQUESTION_OPTIONS).get(self.request_from)
    
    def get_request_status(self):
        return dict(REQUESTION_STATUS_OPTIONS).get(self.request_status)
    
    def get_request_door(self):
        return dict(DOOR_STATUS).get(self.request_door)
    
    def get_failure_reason(self):
        return dict(FAILURE_REASON).get(self.failure_reason)
        