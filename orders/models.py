from django.db import models
from django.contrib.auth.models import User



AILMENT_CHOICES = ( 
    ("HIV", "HIV"),
    ("HYPERTENSION", "hypertension"),
    ("DIABETES", "diabetes"), 
)


class Medication(models.Model):
    '''
    Handles medications available in the health facility
    '''
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)
    
    
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    '''
    Handles customers
    '''
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    address = models.CharField(max_length=255)
    condition = models.CharField(max_length=255,choices = AILMENT_CHOICES, default='')
    
    def __str__(self):
        return self.user.username
    

class Order(models.Model):
    '''
    Handles customer orders
    '''
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    medications = models.ForeignKey(Medication, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)
    order_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.customer} - {self.medication}"
    

class Statement(models.Model):
    '''
    Handles statements
    '''
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)
    
    def __str__(self):
        return f"Statement for {self.customer}"  