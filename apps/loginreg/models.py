from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirmation):
        errors = []
        if len(first_name) < 2:
            errors.append('First name must be at least two characters!')
        if len(last_name) < 2:
            errors.append('Last name must be at least two characters!')
        if not first_name.isalpha() or not last_name.isalpha():
            errors.append('Name must be alphabetic!')
        if len(email) == 0:
            errors.append('Email is required!')
        if not EMAIL_REGEX.match(email):
            errors.append('Invalid email!')
        if len(password) < 8:
            errors.append('Password must be at least eight characters!')
        if password != confirmation:
            errors.append('Password and confirmation must match!')
        if len(errors) is not 0:
            return (False, errors)
        else:
            u = self.create(first_name=first_name, last_name=last_name, email=email, password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
            u.save()
            return (True, u)

    def login(self, email, password):
        errors = []
        if not EMAIL_REGEX.match(email):
            errors.append('Invalid email!')
            return (False, errors)
        u = self.all().filter(email=email)[:1]
        if not u[0]:
            errors.append('Invalid email or password')
            return (False, errors)
        if not bcrypt.hashpw(password.encode('utf-8'), u[0].password.encode('utf-8')):
            errors.append('Invalid email or password')
            return (False, errors)
        else:
            return (True, u[0])

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    manager = UserManager()
