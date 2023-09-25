from django import forms
from django.forms import ModelForm
from .models import Student, Question


class RegisterForm(ModelForm):
	class Meta:
		model=Student
		fields=('name', 'registering_for',)
		widgets={

			    'name':forms.TextInput(attrs={'class':'form-control', 'style':'color:white;', 'placeholder':'Name *', 'type':'text', 'name':'your-name'}),
			    'registering_for':forms.Select(attrs={'class':'form-control', 'placeholder':'category', 'required':'True', 'name':'category'}),
			}
		labels={

			    'name':'Name',
			    'registering_for':'Class',
			    }

class QuestionForm(ModelForm):
	class Meta:
		model=Question
		fields=('question',)
		widgets={

			    'question':forms.TextInput(attrs={'class':'form-control', 'style':'color:white;', 'placeholder':'Ask question here *', 'type':'text', 'name':'your-name'}),
			}
		labels={

			    'question':'Question',
			    
			    }