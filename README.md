django-demo-reset
=================

App which resets all models dates relative to a previous demo date.

This is useful if you want to 'replay' the same demo over and over again,
as you can update the dates on all your models to be within the current
period.

Eg, if you have an app with meeting appointments, set up 4 weeks ago, you can
run this app's management command specifying the date it was setup, and it
will update all date and datetime fields, adding 4 weeks to their value
(whatever it is).

The rebasing is performed by calling the django management command
'rebase_date_fields', eg:

```shell
python project/manage.py rebase_date_fields 2013-02-24
```

Specifying fields to ignore
---------------------------

You can specify certain fields to ignore if you prefer some of your fields not
to be updated. Simply add the class and field names you don't want updated to
a setting called ``DEMO_DATE_RESET_IGNORES``, with this format:

```python
  DEMO_DATE_RESET_IGNORES = {
        'django.contrib.auth.models.User': [ 'last_login', 'date_joined' ]
        }
```
