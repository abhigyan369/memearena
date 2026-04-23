from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from memes.models import Meme
from .models import Vote

@login_required
def vote(request, meme_id, value):
    if request.method != 'POST':
        return HttpResponseForbidden()
    
    meme = get_object_or_404(Meme, id=meme_id)
    
    try:
        existing_vote = Vote.objects.get(user=request.user, meme=meme)
        if existing_vote.value == value:
            existing_vote.delete()
        else:
            existing_vote.value = value
            existing_vote.save()
    except Vote.DoesNotExist:
        Vote.objects.create(user=request.user, meme=meme, value=value)
        
    # Important: To update the score live, you've to refetch the meme or clear its cache
    # But django does it perfectly upon hitting the property getter in the template again.
    return render(request, 'votes/vote_buttons.html', {'meme': meme})
