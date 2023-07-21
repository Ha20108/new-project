from django.db import models
from django.contrib.auth.models import User



class Router(models.Model):
    host = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.first().id)  # إضافة حقل "user"

    def __str__(self):
        return self.name


