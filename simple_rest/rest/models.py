# -*- coding: utf-8 -*-
# Define a custom User class to work with django-social-auth
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    objects = UserManager()
    gender = models.CharField(u'Пол', max_length=15, blank=True, null=True)    
    birthdate = models.DateField(u'Дата рождения', blank=True, null=True)
    
    def calculate_age(self):
        if not self.birthdate:
            return 0
        born = self.birthdate
        today = date.today()
        try: 
            birthday = born.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, month=born.month+1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year
