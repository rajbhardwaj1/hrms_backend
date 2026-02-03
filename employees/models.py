from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
