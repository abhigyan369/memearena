from rest_framework import serializers
from users.models import CustomUser
from memes.models import Meme, Tag
from comments.models import Comment
from votes.models import Vote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'meme', 'author', 'parent', 'body', 'created_at']
        read_only_fields = ['author', 'created_at']

class VoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Vote
        fields = ['id', 'user', 'meme', 'value', 'created_at']
        read_only_fields = ['user', 'created_at']

class MemeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    score = serializers.ReadOnlyField()
    hot_score = serializers.ReadOnlyField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Meme
        fields = ['id', 'title', 'caption', 'image', 'author', 'tags', 'score', 'hot_score', 'comments_count', 'slug', 'created_at']
        read_only_fields = ['author', 'slug', 'created_at', 'score', 'hot_score']

    def get_comments_count(self, obj):
        return obj.comments.count()
