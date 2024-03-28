from django.db import models
from django.contrib.auth.models import User



AILMENT_CHOICES = ( 
    ("HIV", "HIV"),
    ("HYPERTENSION", "hypertension"),
    ("DIABETES", "diabetes"), 
)



MEDICINE_CHOICES = ( 
    ("MED1", "med1"),
    ("MED2", "med2"),
    ("MED3", "med3"), 
)

MEDICINE_PRICES = {
    "MED1": 5.00,
    "MED2": 10.00,
    "MED3": 15.00,
}

class Medication(models.Model):
    '''
    Handles medications available in the health facility
    '''
    name = models.CharField(max_length=255, choices=MEDICINE_CHOICES, default='')
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.name in dict(MEDICINE_CHOICES):
            selected_price = MEDICINE_PRICES.get(self.name)
            self.price = selected_price
        else:
            print("Medication name not in choices:", self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f" {self.name} - {self.price}"

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
    medications = models.ManyToManyField(Medication)
    order_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_total_price(self):
        total_price = sum(medication.price * medication.quantity for medication in self.medications.all())
        print("Total Price:", total_price) 
        return total_price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the order first
        self.total_price = self.calculate_total_price()
        print("Total Price before saving:", self.total_price)
        super().save(*args, **kwargs)  # Save again to update total_price

    def __str__(self):
        medications_str = ', '.join(str(medication) for medication in self.medications.all())
        return f"{self.customer} - Medications: {medications_str}, Total Price: {self.total_price}"

    
class Statement(models.Model):
    '''
    Handles statements
    '''
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)
    
    def __str__(self):
        return f"Statement for {self.customer}"  