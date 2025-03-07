from django.db import models

# Create your models here.
main_category = [('Phone','Phone'), ('Laptop', 'Laptop')]

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    stock = models.IntegerField()
    active = models.BooleanField(default=True)
    category = models.CharField(max_length = 100, null=True, blank=True, choices=main_category)
    
    def __str__(self):
        return self.name
