from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from memes.models import Meme
from .models import Comment
from .forms import CommentForm

@require_POST
@login_required
def add_comment(request, meme_id, parent_id=None):
    meme = get_object_or_404(Meme, id=meme_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.meme = meme
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id, meme=meme)
            comment.parent = parent_comment
        comment.save()
        
    return redirect('meme_detail', slug=meme.slug)
