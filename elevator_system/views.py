from django.http import HttpResponse
from django.views import View
from .models import Elevator, STATUS, ElevatorTravelLog, DOOR_STATUS, REQUESTION_OPTIONS, FAILURE_REASON
from django.core.cache import cache
from django.db.models.functions import Abs
from django.db.models import F

status_dict = dict(STATUS)
door_status_dict = dict(DOOR_STATUS)
status_dict_mapping = { v: k for k, v in status_dict.items() }
door_status_mapping = { v: k for k, v in door_status_dict.items() }


#basic create elevator view
class AddElevator(View):
    def get(self, request):
        e = Elevator.objects.create()
        e.save()
        return HttpResponse('New Elevator added')

#To check and change the status of elevator
class ElevatorStatus(View):
    #to check the status of the elevator
    def get(self, request, id):
        e = Elevator.objects.filter(id = id)
        if len(e) == 0:
            return HttpResponse('Elevator does not exist')
        
        elevator = e.first()
        elevator_status = status_dict.get(elevator.status, 1)
        return HttpResponse('Status of elevator  - %s' % elevator_status)
    
    #to change the status of the elevator
    def post(self, request, id):
        status = request.POST.get('status', None)
        if not status:
            return HttpResponse('please enter a valid status')
        
        status_value = status_dict_mapping.get(status, None)
        if not status_value:
            return HttpResponse('please enter a valid status')

        e = Elevator.objects.filter(id = id)
        if len(e) == 0:
            return HttpResponse('Elevator does not exist')
        elevator = e.first()
        elevator.status = status_value
        elevator.save()
        return HttpResponse('Updated status of Elevator ' + str(elevator.id) + ' - ' + status)

#Accept user request to open or close the door from inside the elevator
#Note that this discuss is only valid for 30 seconds, the elevator will close again
#Also saves the elevator request log
class ElevatorDoorStatus(View):
    def get(self, request, id, door_status = None):
        e = Elevator.objects.filter(id = id)
        if len(e) == 0:
            return HttpResponse('Elevator does not exist')
        
        elevator = e.first()
        
        status_mapping = cache.get("door_status", None)
        if not door_status:
            if not status_mapping or status_mapping.get(elevator.id, None) == None:
                return HttpResponse(' Elevator ' + str(elevator.id) + ' is Closed')
            return HttpResponse(' Elevator ' + str(elevator.id) + ' is ' + status_mapping.get(elevator.id, 'Closed').title())
        
        if status_mapping == None:
            status_mapping = {}

        if door_status not in ['close', 'open']:
            return HttpResponse('Invalid door status')
        
        status_mapping[elevator.id] = door_status
        cache.set("door_status", status_mapping, timeout=30)
        travel_log = ElevatorTravelLog.objects.create(elevator_id=elevator, request_from=2, request_status=1, 
                        request_door=door_status_mapping.get(door_status, None))
        travel_log.save()
        return HttpResponse('Updated door request of Elevator ' + str(elevator.id) + ' - ' + door_status.title())

#to handle the elevator request and also display all travel logs of an elevator
class ElevatorTravel(View):
    #handling the request for elevator 
    #if the user is outside the elevator, we will call the closest elevator 
    #once user enters the elevator, we track the request and move the elevator to user's demanded floor
    def post(self, request):
        elevator_id = request.POST.get('elevator_id', None)
        floor_from = request.POST.get('floor_from', None)
        floor_to = request.POST.get('floor_to', None)

        if not floor_to:
            return HttpResponse('Invalid floor entered')  
        
        floor_to = int(floor_to)
        
        if not elevator_id and not floor_from:
            elevators = Elevator.objects.filter(status = 1).annotate(abs_floor = Abs(F('floor') - 5)).order_by('abs_floor')
            if len(elevators) == 0:
                travel_log = ElevatorTravelLog.objects.create(elevator_id=None, request_from=1, request_status=2, 
                        failure_reason=1)
                travel_log.save()
                return HttpResponse("None of the Elevators in available")
            elevator = elevators.first()
            floor_from = elevator.floor
            elevator.floor = floor_to
            
            if floor_to > floor_from:
                elevator.last_travel_direction = 1
            else:
                elevator.last_travel_direction = 2
            elevator.save()

            travel_log = ElevatorTravelLog.objects.create(elevator_id = elevator, request_from = 1, request_status = 1, 
                        floor_from = floor_from, floor_to = floor_to)
            travel_log.save()
            return HttpResponse('Elevator ' + str(elevator.id) + ' is coming to floor ' + str(floor_to))
        
        if None in [elevator_id, floor_from]:
            return HttpResponse('Missing data from request')
        
        elevators = Elevator.objects.filter(id = elevator_id)
        if len(elevators) == 0:
            return HttpResponse("Invalid Elevator id")

        elevator = elevators.first()
        floor_from = elevator.floor
        elevator.floor = floor_to
        if floor_to > floor_from:
            elevator.last_travel_direction = 1
        else:
            elevator.last_travel_direction = 2
        elevator.save()

        travel_log = ElevatorTravelLog.objects.create(elevator_id = elevator, request_from = 2, request_status = 1, 
                        floor_from = floor_from, floor_to = floor_to)
        travel_log.save()
        return HttpResponse('Elevator ' + str(elevator.id) + ' is coming to floor ' + str(floor_to))
    
    #get all logs of travel of a elevator
    def get(self, request):
        elevator_id = request.GET.get('elevator_id', None)
        data = []
        
        if elevator_id:
            elevators = Elevator.objects.filter(id = elevator_id)
            if len(elevators) == 0:
                return HttpResponse("Invalid Elevator id")
            elevator = elevators.first()
            travel_logs = ElevatorTravelLog.objects.filter(elevator_id = elevator)
        else:
            travel_logs = ElevatorTravelLog.objects.all()
        
        travel_logs = travel_logs.order_by('-created_at')

        for log in travel_logs:
        
            dt = 'Button pressed from ' + log.get_request_from().title()
            if log.failure_reason:
                dt += ', failure reason: ' + log.get_failure_reason()
                data.append(dt)
                continue

            if log.elevator_id:
                dt += ', elevator - ' + str(log.elevator_id)

            if log.request_door:
                dt += ', Requested door to ' + log.get_request_door().title()
                data.append(dt)
                continue

            if log.floor_to:
                dt += ', floor to ' + str(log.floor_to)
            if log.floor_from:
                dt += ', floor from ' + str(log.floor_from)
            
            data.append(dt)
        
        result = '\n'.join(data)
        return HttpResponse(result)


#return current floor and last direction of travel for the elevator    
class ElevatorCurrentStatus(View):
    def get(self, request, id):
        e = Elevator.objects.filter(id = id)
        if len(e) == 0:
            return HttpResponse('Elevator does not exist')
        
        elevator = e.first()
        return HttpResponse("Elevator - " + str(elevator.id) + " is at floor " + str(elevator.floor) + " for which it travelled in direction - " + str(elevator.get_last_travel_direction()) )



            
                




        
