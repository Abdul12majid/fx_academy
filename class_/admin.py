from django.contrib import admin
from .models import Package, Student, Question, Message

# Register your models here.
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
	list_display=('name', 'price',)
	list_filter=('name',)

@admin.register(Student)
class PackageAdmin(admin.ModelAdmin):
	list_display=('name', 'registering_for', 'date_registered',)
	list_filter=('name',)

@admin.register(Question)
class PackageAdmin(admin.ModelAdmin):
	list_display=('question', 'date_asked',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display=('name', 'message', 'date_sent',)