from django.urls import path, register_converter
from . import views


class SignedIntConverter:
    regex = '-?[0-9]+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


register_converter(SignedIntConverter, 'sint')


urlpatterns = [
    path('<int:meme_id>/<sint:value>/', views.vote, name='vote'),
]