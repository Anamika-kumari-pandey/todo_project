from django.db import models

class UserDetail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)  # 👈 Link each task to a user
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
