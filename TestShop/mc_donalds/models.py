from django.db import models
from datetime import datetime
from mc_donalds.resourses import *


class Order(models.Model):
    time_in = models.DateTimeField(auto_now=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (datetime.now() - self.time_in).total_seconds() // 60


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)


class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.Split()[0]


class ProductOrder(models.Model):
    _amount = models.IntegerField(default=1, db_column="amount")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    in_order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def product_sum(self):
        product_price = self.product.price
        return self.amount * product_price

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        save()


# prod1 = Product(name='Витая пара', price=933)
# prod1.save()
#
# prod2 = Product.objects.create(name='Клавиатура', price=1060)
