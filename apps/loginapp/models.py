from django.contrib.auth.models import AbstractUser
from django.db import models

class MyCustomUser(AbstractUser):
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
