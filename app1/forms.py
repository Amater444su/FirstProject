from django import forms
from .models import Product, Comment, Profile # Message


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'text', 'price', 'image', 'type']

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    phone_number = forms.CharField()

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'address', 'phone_number', 'profile_image']

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


# class MessageForm(forms.ModelForm):
#
#     class Meta:
#         model = Message
#         fields = ['topic', 'text']
#
#     def __init__(self,  *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'

