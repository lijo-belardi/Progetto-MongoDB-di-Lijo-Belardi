from django import forms


class OrderForm(forms.Form):
    price = forms.FloatField(widget=forms.TextInput(attrs={'class': 'dark-text'}))
    quantity = forms.FloatField(widget=forms.TextInput(attrs={'class': 'dark-text'}))

    def clean(self):
        cleaned_data = super().clean()
        price = self.cleaned_data.get('price')
        quantity = self.cleaned_data.get('quantity')
        if price < 0:
            raise forms.ValidationError('') #display messages.error instead
        if quantity < 0:
            raise forms.ValidationError('') #display messages.error instead
        return cleaned_data