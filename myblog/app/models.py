from django.db import models

# Create your models here.
class author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=10,default='defaultpassword')


class blogs(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    aid = models.ForeignKey(author, on_delete=models.CASCADE, default=1)

