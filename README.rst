===========
bundy clock
===========

Bundy clock simple Django app for storing and retrieving punch times,
to be used with the lock screen saver bundy clock:
https://github.com/dahallgren/bundyclock

Quick start
-----------

1. Add "bundyclock" to your INSTALLED_APPS setting like this
along with django rest framework::

    INSTALLED_APPS = [
        ...
        'bundyclock',
        'rest_framework',
    ]

2. Include the bundyclock URLconf in your project urls.py like this::

    path('bundyclock/', include('bundyclock.urls')),

3. Run `python manage.py migrate` to create the bundyclock models.

4. Visit http://127.0.0.1:8000/bundyclock/api/
