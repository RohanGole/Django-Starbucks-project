from django.db import models
from django.contrib.auth.models import User
 
# Create your models here.
class items(models.Model):
    CAT=(1,'Our Special'),(2,'Creamy'),(3,'Chocolate')
    name=models.CharField(max_length=50)
    price=models.FloatField()
    cdetails=models.CharField(max_length=1000)
    cat=models.IntegerField()
    is_active=models.BooleanField(default=True)
    cimage=models.ImageField(upload_to='image')

    def _str_(self):
        return self.name

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    cid=models.ForeignKey(items,on_delete=models.CASCADE,db_column="cid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    Order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    cid=models.ForeignKey(items,on_delete=models.CASCADE,db_column="cid")
    qty=models.IntegerField(default=1)     

class ordertable(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phoneno=models.FloatField()
    noofcoffee=models.IntegerField()
    address=models.CharField(max_length=1000)       


# models.py
# class CustomerReview(models.Model):
#     name = models.CharField(max_length=100)
#     rating = models.IntegerField()
#     review_text = models.TextField()

#     def _str_(self):
#         return self.name    

# models.py
class CustomerReview(models.Model):
    customer_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name