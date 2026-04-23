from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Meme(models.Model):
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='memes/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memes')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='memes', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    @property
    def score(self):
        # We will aggregate votes or calculate it here
        # Assuming related_name for Vote will be 'votes'
        upvotes = self.votes.filter(value=1).count()
        downvotes = self.votes.filter(value=-1).count()
        return upvotes - downvotes

    def get_hot_ranking(self):
        """
        Hot Ranking Algorithm (Hacker News inspired)
        Score = (upvotes - downvotes - 1) / (Age in hours + 2)^1.5
        """
        s = self.score
        # Calculate age in hours
        age_delta = timezone.now() - self.created_at
        age_hours = age_delta.total_seconds() / 3600
        
        # Penalize if score is less than 0
        if s == 0:
            return 0
        
        return (s - 1) / pow((age_hours + 2), 1.8)

    def __str__(self):
        return self.title

class MemeOfDay(models.Model):
    date = models.DateField(unique=True)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='featured_days')

    def __str__(self):
        return f"Meme of {self.date}"
