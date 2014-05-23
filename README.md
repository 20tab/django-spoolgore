django-spoolgore
================

A django email backend for the Spoolgore daemon

To use it you have to configure the email backend in  your project settings.py:

```py
EMAIL_BACKEND = 'spoolgore.backend.EmailBackend'
```

then you need to configure the directory where Spoolgore is spooling:

```py
SPOOLGORE_DIRECTORY = '/var/spool/foobar'
```
