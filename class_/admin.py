from django.contrib import admin
from .models import Package, Student

# Register your models here.
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
	list_display=('name', 'price',)
	list_filter=('name',)

@admin.register(Student)
class PackageAdmin(admin.ModelAdmin):
	list_display=('name', 'registering_for', 'date_registered',)
	list_filter=('name',)