from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Meme, MemeOfDay

@shared_task
def pick_meme_of_the_day():
    today = timezone.localtime(timezone.now()).date()
    yesterday = timezone.now() - timedelta(days=1)
    
    if MemeOfDay.objects.filter(date=today).exists():
        return "Meme of the Day already selected."

    top_meme = Meme.objects.filter(created_at__gte=yesterday) \
        .annotate(vote_score=Coalesce(Sum('votes__value'), 0)) \
        .order_by('-vote_score', '-created_at').first()
        
    if top_meme:
        MemeOfDay.objects.create(date=today, meme=top_meme)
        return f"Selected '{top_meme.title}' as Meme of the Day for {today}."
    else:
        fallback = Meme.objects.annotate(vote_score=Coalesce(Sum('votes__value'), 0)) \
            .order_by('-vote_score', '-created_at').first()
        if fallback:
            MemeOfDay.objects.create(date=today, meme=fallback)
            return f"Selected fallback '{fallback.title}' as Meme of the Day for {today}."
        
    return "No memes available."
