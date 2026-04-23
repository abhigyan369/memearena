from django import template

register = template.Library()

@register.simple_tag
def user_vote_value(meme, user):
    if not user.is_authenticated:
        return 0
    # Avoid extra DB queries if votes are prefetched.
    # Otherwise `.all()` fetches them once and caches in the instances.
    for v in meme.votes.all():
        if v.user_id == user.id:
            return v.value
    return 0

@register.filter
def dankness(score):
    if score is None:
        score = 0
    if score < 10: return "Normie"
    if score < 50: return "Dank"
    if score < 100: return "Spicy 🌶"
    return "GOD TIER 👑"
