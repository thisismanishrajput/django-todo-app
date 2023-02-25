from django.db import models
from account.models import User


class TodoModel(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=255,null=True)
    created_by = models.ForeignKey(User,related_name='todos',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
