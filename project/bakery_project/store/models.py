from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'users'  # This tells Django to use the existing MySQL table
        managed = False     # Important! Prevents Django from managing the table (no CREATE or ALTER)

    def __str__(self):
        return self.username

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')  # make sure media setup is done

    def __str__(self):
        return self.name
