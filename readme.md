# Locksmith
Locksmith is a password management application.  Think of it as a lightweight
open source web based 1password or keepass.

Visit #locksmith-io on IRC (freenode) for questions, help, etc.

Screenshots [here](https://github.com/ehazlett/locksmith/wiki/Screenshots)

# Setup

* `pip install -r requirements.txt`
* `python manage.py syncdb --noinput`
* `python manage.py migrate`
* `python manage.py createsuperuser`
* `python manage.py runserver`

# Application Settings

Edit all application settings in `settings.py`.  You can also create a
`local_settings.py` with override values.

# License
Apache License 2.0
