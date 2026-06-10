from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    staff_id = models.CharField(max_length=20, unique=True)
    
    
    REQUIRED_FIELDS = ['staff_id']
    
    def __str__(self):
        return self.username

