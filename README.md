# elevator_system
Note: Please note that mistakenly i missed the part of creating a repo on git for this project, hence there is a single commit.

Steps to set up this project
1. create and activate virtual environment
   -> source es/bin/activate

2. set up redis cache and postgres on your local and modify the settings accordingly (CACHE and DATABASES)
   -> pip install django-redis

3. set up data in postgres
   -> python manage.py makemigrations
   -> python manage.py migrate

4. create elevator data for 5 elevators
    call the elevator api 5 times 
            or 
   -> python manage.py shell
   -> for i in range(0, 5):
        e = Elevator.objects.create()
        e.save() 

5. To access data from admin panel
   -> python manage.py createsuperuser

Architecture, Repository file structure, Database modelling

# Assumptions:
1. Number of elevators in the system will be defined by the API to intialise the elevator system
2. Elevator System has got only one button per floor.
So if there are a total of 5 floors, there will be 5 buttons per floor.
4. Note that, this doesn't not mimic real world, when you would have a total of 10 buttons for 5 floors ( one for up and one for down)
5. Once the elevator reaches its called point, then based on what floor is requested, it moves either up or down.

Architecture:
1. Includes a elevator db which has a unique id(to identify the elevator from which the request came in), status(working status of the elevator), current_floor, last_travel_direction(will tell which direction elevator travelled to reach the current floor)

2. Based on above data, once we get an request from outside the elevators, we figure out the closest elevator to the floor and send that elevator

3. for open and close command: we are using the concept of real world elevators. If an open command comes in from inside an elevator, the elevator door will remain open for 30 sec and then will change to close
this data is set up in redis cache

4. All instructures and elevator travels are saved in a table 'eleavtorTravelLog'


# Repository file structure:
Basic file structure for this project is used:
elevator_system contains
1. models -> to design the db we are gonna use
2. views -> api and logic for them
3. urls-> api defination
4. admin -> can access /admin to change any properties of elevator


# Database modelling
1. Elevator -> fields: id(unique elevator id), floor(default = 0, Integer), status (working, in maintainace, not working), last_travel_direction(up, down)

2. ElevatorTravelLog -> fields: elevator_id(from above db), request_from(Inside, outside), request_status(success, failure), request_door(close, open), failure_reason (list of all the reasons for failure), floor_from, floor_to, created_at(saving time of request)

# Api's
doc link with screenshot:
https://docs.google.com/document/d/1TLcbo8OKLvuhDhDfwB1QoGi8Sw68RB8q4nxyz73ZYUg/edit
