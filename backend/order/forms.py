from django import forms 
from .models import EventOrder
from schedule.models import Event

class CreateOrderForm(forms.Form):

    class Meta:
        model = EventOrder
        fields = ('fullname', 'phone_number','email', 'quantity','payment_by_card',)


    fullname = forms.CharField()
    phone_number = forms.CharField()
    email = forms.CharField()
    quantity = forms.IntegerField()
    payment_by_card = forms.ChoiceField(
        choices=[
            ('0', 'False'),
            ('1', 'True')
        ],
    )