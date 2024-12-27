from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyCustomUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# Create your models here.
class MyCustomUser(AbstractBaseUser):
   email = models.EmailField(unique=True)
   first_name = models.CharField(max_length=30, blank=True)
   last_name = models.CharField(max_length=30, blank=True)
   is_active = models.BooleanField(default=True)
   is_admin = models.BooleanField(default=False)
   timezone = models.CharField(max_length=30, default='UTC')
   is_custom = models.BooleanField(default=False)
   is_staff = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   objects = MyCustomUserManager()
   USERNAME_FIELD = 'email'
   EMAIL_FIELD = 'email'
   def __str__(self):
       return self.email
   def has_perm(self, perm, obj=None):
       return True
   def has_module_perms(self, app_label):
       return True
   @property
   def is_utc(self):
       return self.timezone == 'UTC'


from django import forms
from django.db import models
from django.views.generic.edit import FormView
from django.shortcuts import render

# Define o modelo
class FlexaoNormalSimplesRetangularModel(models.Model):
    fck = models.IntegerField(choices=[(x, x) for x in [20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90]], default=25)
    fyk = models.IntegerField(choices=[(x, x) for x in [250, 500, 600]], default=500)
    es = models.IntegerField(choices=[(x, x) for x in [190, 200, 215]], default=200)
    gamac = models.FloatField(default=1.4)
    gamas = models.FloatField(default=1.15)
    gamaf = models.FloatField(default=1.4)
    bduct = models.FloatField(default=1.0)
    b = models.FloatField(default=15)
    h = models.FloatField(default=40)
    d = models.FloatField(default=36)
    amk = models.FloatField(default=30)

    @property
    def dl(self):
        return self.h - self.d


