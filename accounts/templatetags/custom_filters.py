from django import template

register = template.Library()

@register.filter
def is_following(user, target_user):
    """
    Returns True if 'user' is following 'target_user'
    """
    return user.following.filter(following=target_user).exists()
@register.filter
def dict_get(d, key):
    if d is None:
        return False
    return d.get(key)