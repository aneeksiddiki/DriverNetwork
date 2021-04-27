from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Car,Customer,Renter

class AddCar(ModelForm):
    def __init__(self,*args,**kwargs):
        super(AddCar,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
    class Meta:
        model = Car
        fields = '__all__'

class SignUpMember(ModelForm):
    def __init__(self,*args,**kwargs):
        super(AddCar,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
    class Meta:
        model = Customer
        fields = '__all__'

class CreateRenter(ModelForm):
    def __init__(self,*args,**kwargs):
        super(CreateRenter,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
    class Meta:
        model = Renter
        fields = '__all__'