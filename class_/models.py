from django.db import models

# Create your models here.
class Package(models.Model):
	name=models.CharField(max_length=50, blank=True)
	price=models.IntegerField()

	def __str__(self):
		return f'{self.name} for ${self.price}'

class Student(models.Model):
	name=models.CharField(max_length=50, blank=True)
	registering_for=models.ForeignKey(Package, on_delete=models.CASCADE)
	date_registered=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.name}'