from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Meme, MemeOfDay, Tag
from .forms import MemeForm

class RandomMemeView(RedirectView):
    permanent = False
    
    def get_redirect_url(self, *args, **kwargs):
        random_meme = Meme.objects.order_by('?').first()
        if random_meme:
            return reverse_lazy('meme_detail', kwargs={'slug': random_meme.slug})
        return reverse_lazy('latest_memes')

class LatestMemeListView(ListView):
    model = Meme
    template_name = 'memes/meme_list.html'
    context_object_name = 'memes'
    paginate_by = 12

    def get_queryset(self):
        return Meme.objects.select_related('author').prefetch_related('tags').order_by('-created_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_title'] = 'Latest Memes'
        today = timezone.localtime(timezone.now()).date()
        mod = MemeOfDay.objects.filter(date=today).select_related('meme', 'meme__author').first()
        if mod:
            context['featured_meme'] = mod.meme
        return context

class TrendingMemeListView(ListView):
    model = Meme
    template_name = 'memes/meme_list.html'
    context_object_name = 'memes'
    paginate_by = 12

    def get_queryset(self):
        memes = list(Meme.objects.select_related('author').prefetch_related('tags').all())
        memes.sort(key=lambda m: m.get_hot_ranking(), reverse=True)
        return memes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_title'] = 'Trending Memes'
        return context

class MemeDetailView(DetailView):
    model = Meme
    template_name = 'memes/meme_detail.html'
    context_object_name = 'meme'

class MemeCreateView(LoginRequiredMixin, CreateView):
    model = Meme
    form_class = MemeForm
    template_name = 'memes/meme_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('meme_detail', kwargs={'slug': self.object.slug})

class BaseTopListView(ListView):
    model = Meme
    template_name = 'memes/meme_list.html'
    context_object_name = 'memes'
    paginate_by = 12

    def get_queryset(self):
        qs = Meme.objects.select_related('author').prefetch_related('tags')
        time_filter = self.get_time_filter()
        if time_filter:
            qs = qs.filter(created_at__gte=time_filter)
        
        return qs.annotate(vote_score=Coalesce(Sum('votes__value'), 0)).order_by('-vote_score', '-created_at')

    def get_time_filter(self):
        return None

class TopTodayListView(BaseTopListView):
    def get_time_filter(self):
        return timezone.now() - timedelta(days=1)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_title'] = 'Top Today'
        return context

class TopWeekListView(BaseTopListView):
    def get_time_filter(self):
        return timezone.now() - timedelta(days=7)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_title'] = 'Top Week'
        return context

class AllTimeTopListView(BaseTopListView):
    def get_time_filter(self):
        return None
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_title'] = 'All Time Hits'
        return context

class TagMemeListView(BaseTopListView):
    def get_time_filter(self):
        return None
        
    def get_queryset(self):
        qs = super().get_queryset()
        self.tag_slug = self.kwargs.get('slug')
        return qs.filter(tags__slug=self.tag_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'tag_slug'):
            tag_obj = get_object_or_404(Tag, slug=self.tag_slug)
            context['feed_title'] = f'#{tag_obj.name}'
        return context
