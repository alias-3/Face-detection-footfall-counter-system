# Footfall counter system
# Execution Guide:

Note : It requires a fully functional webcam for operation.

Youtube Link -https://www.youtube.com/watch?v=WI7hdncyUuw

counter-system Our Implementation:-

1)For our project two cameras are required one camera is top-down camera which counts all incoming and outgoing people(even employees) {On our website this can be done using Startcount Button.

2)Another camera is used which faces the people entering the store it detects employees this can be done in our website using Test button.

3)Now total footfall are counted using = total people entered - employees entered . This will give us the exact footfall count.

4)To add new employee the is a button on our website Add Employee . This is a prototype we have not added Analytics which will be added in later stages.

5)Database used is sqlite.Criminal is detected if the face matches with criminal database.

# Installation Guide:

Install Django, dlib and opencv-contrib-python

Run Django project

Go to the root directory

Run command:- python manage.py runserver
