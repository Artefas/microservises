
from django import forms
from django.forms import IntegerField, CharField

class TrainForm(forms.Form):

    train_id = IntegerField(
                        label="ID поезда",
                        widget=forms.NumberInput(attrs={'readonly':'readonly'})
                    )
    train_number = CharField(
                        label="Номер поезда",
                        widget=forms.TextInput(attrs={'readonly': 'readonly'})
                    )
    from_city = CharField(
                        label="Откуда",
                        widget=forms.TextInput(attrs={'readonly': 'readonly'})
                    )
    to_city = CharField(
                        label="Куда",
                        widget=forms.TextInput(attrs={'readonly': 'readonly'})
                    )

    ticket_price = IntegerField(
                        label="Цена билета",
                        widget=forms.NumberInput(attrs={'readonly': 'readonly'})
                    )
    total_places = IntegerField(
                        label="Всего мест",
                        widget=forms.NumberInput(attrs={'readonly': 'readonly'})
                    )
    free_places = IntegerField(
                        label="Осталось мест",
                        widget=forms.NumberInput(attrs={'readonly': 'readonly'})
                    )
    date = CharField(
                        label="Дата отправления",
                        widget=forms.TextInput(attrs={'readonly': 'readonly'})
                    )
    time = CharField(
                        label="Время отправления",
                        widget=forms.TextInput(attrs={'readonly': 'readonly'})
                    )

    ticket_count = IntegerField(
                        widget=forms.NumberInput(attrs={'type':'hidden', 'value':'1'},)
                    )


class UserForm(forms.Form):
    user_id = IntegerField(
        label="ID пользователя",
        widget=forms.NumberInput(attrs={'readonly': 'readonly'})
    )
    name = CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

class UserEditForm(forms.Form):
    user_id = IntegerField(
        label="ID пользователя",
        widget=forms.NumberInput(attrs={'readonly': 'readonly'})
    )
    name = CharField(
        label="Введите новое имя",
        widget=forms.TextInput()
    )

class BillingForm(forms.Form):

    card = IntegerField(
        label="Введите номер карты"
    )

    name = CharField(
        label="Имя держателдя карты"
    )

    price = IntegerField(
        label="Сумма к оплате",
        widget=forms.NumberInput(attrs={'readonly': 'readonly'})
    )
    order_id = IntegerField(
        widget=forms.NumberInput(attrs={'type':'hidden', 'readonly': 'readonly'})
    )







