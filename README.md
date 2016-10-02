# messenger
This app is written on python3 

This is the setup rules:    
    pip install -r requirements( I recommend you use virtualenv :)) )
    python3 manage migrate (it is a must)

I guess you know how to run django inbuilt server but in case:
    python3 manage.py runserver (I have left debug=True)

I have made some design changes because there was a lack of some mockups of pages.

There are things that I did not do (to meet production requirements) due to my tight schedule :/ But I can assure you I am capable of doing them :)

Things to add or improve:
    * Responsive design compatibility with more mobile phones (now its best for high rez phones or tablets :( )
    * Unit tests
    * Some views
    * Real time messages page updates with AJAX
    * Django application prepared for gunicorn and nginx / apache and uwsgi
    * DB change (to any other NoSql or Sql)
    * asynchronous apis for sending messages
    * etc..  

I hope you like it :)