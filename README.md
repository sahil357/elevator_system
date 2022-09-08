# elevator_system
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