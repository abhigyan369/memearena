from django.db import models
from django.conf import settings

class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    meme = models.ForeignKey('memes.Meme', on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'meme'], name='unique_vote_per_user_meme')
        ]

    def __str__(self):
        return f"{self.user.username} voted {self.value} on {self.meme.title}"
