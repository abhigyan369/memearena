from django import forms
from django.core.exceptions import ValidationError
from .models import Meme, Tag
import os

class MemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['title', 'caption', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2'}),
            'caption': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'tags': forms.SelectMultiple(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # 5MB Limit
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 5MB limit )")
            
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            if ext not in valid_extensions:
                raise ValidationError("Unsupported file extension. We only support standard image formats (jpg, png, gif, webp).")
        return image
