from django.db import models
from .category import Category
from django.core.validators import MinLengthValidator

#t = Product(productId = p["productId"] , name = p["productName"], image = p["productImage"], stock  = p["productStock"], price = p["productPrice"], sprice = p["salePrice"], category = p["productCategory"] )...

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return  False

class Product(models.Model):
    productId = models.IntegerField()
    category  = models.ForeignKey(Category, on_delete=models.CASCADE)
    name      = models.CharField(max_length=50)
    image     = models.CharField(max_length=50)
    stock     = models.BooleanField(default=True)
    price     = models.IntegerField(default=0)
    sprice    = models.IntegerField(default=0)
    uid       = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True)
    views     = models.IntegerField(default = 0)

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(productId =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id) 
        else:
            return Product.get_all_products()
    @staticmethod
    def get_all_products_by_customerid(customer_id):
        if customer_id:
            return Product.objects.filter(uid = customer_id) 
        # else:
        #     return Product.get_all_products()
    # @staticmethod
    # def delete_object(pro_id):
    #     if pro_id:
    
    def isExists(self):
        if Product.objects.filter(productId = self.productId):
            return True

        return  False
class Visited(models.Model):
    email = models.EmailField()
    product  = models.IntegerField(null=True)