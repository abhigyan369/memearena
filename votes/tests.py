from django.test import TestCase
from django.db.utils import IntegrityError
from users.models import CustomUser
from memes.models import Meme
from votes.models import Vote

class VoteTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='voter', password='123')
        self.meme = Meme.objects.create(title="Vote check", author=self.user)

    def test_unique_constraint(self):
        """Test unique constraints strictly block duplicate votes inherently."""
        Vote.objects.create(user=self.user, meme=self.meme, value=1)
        
        with self.assertRaises(IntegrityError):
            Vote.objects.create(user=self.user, meme=self.meme, value=1)
