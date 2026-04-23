from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import DetailView
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from .forms import CustomUserCreationForm
from .models import CustomUser

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return get_object_or_404(CustomUser, username=self.kwargs.get('username'))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        
        context['karma'] = user.memes.aggregate(total_score=Coalesce(Sum('votes__value'), 0))['total_score']
        context['total_votes_received'] = user.memes.aggregate(total=Count('votes'))['total']
        context['top_meme'] = user.memes.annotate(vote_score=Coalesce(Sum('votes__value'), 0)).order_by('-vote_score', '-created_at').first()
        context['memes'] = user.memes.all().order_by('-created_at')
        
        return context
