import re
from django import forms 
from django.core.exceptions import ValidationError
from .models import EventOrder

def validate_phone_number_format(value: str) -> None:
    """
    Валидатор для проверки формата номера телефона.
    Номер должен быть в формате XXX-XXX-XX-XX и состоять только из цифр.
    
    Args:
        value (str): Номер телефона для проверки.
        
    Raises:
        ValidationError: Если номер не соответствует формату.
    """
    if not value or not re.match(r'^\d{3}-\d{3}-\d{2}-\d{2}$', value):
        raise ValidationError('Номер телефона должен быть в формате XXX-XXX-XX-XX') 
    

class CreateOrderForm(forms.ModelForm):
    """
    Форма для создания заказа мероприятия.
    """
    class Meta:
        model = EventOrder
        fields = ('fullname', 'phone_number', 'email', 'quantity', 'payment_by_card',)

    payment_by_card = forms.ChoiceField(
        choices=[('0', 'False'), ('1', 'True')],
        widget=forms.RadioSelect,
    )

    def clean_quantity(self) -> int:
        """
        Проверяет количество мест на корректность.
        
        Returns:
            int: Количество мест.
        
        Raises:
            forms.ValidationError: Если количество мест не положительное число.
        """
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Количество должно быть положительным числом.")
        return quantity

    def clean_payment_by_card(self) -> str:
        """
        Проверяет способ оплаты картой на корректность.
        
        Returns:
            str: Способ оплаты картой.
        
        Raises:
            forms.ValidationError: Если значение способа оплаты картой недопустимо.
        """
        payment_by_card = self.cleaned_data['payment_by_card']
        if payment_by_card not in ['0', '1']:
            raise forms.ValidationError("Недопустимое значение для оплаты картой.")
        return payment_by_card
    
    def clean_phone_number(self) -> str:
        """
        Проверяет формат номера телефона.
        
        Returns:
            str: Номер телефона.
        """
        phone_number = self.cleaned_data.get('phone_number')
        validate_phone_number_format(phone_number)
        return phone_number