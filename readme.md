# Locksmith
Locksmith is a password container application.  You can enter account passwords
and Locksmith will encrypt and store them.

# Setup

* `pip install -r requirements.txt`
* `python manage.py syncdb`
* `python manage.py migrate`
* `python manage.py runserver`

# Social Auth
If you want to use Twitter, Google, etc. auth, you need to setup your keys in
`settings.py`.
