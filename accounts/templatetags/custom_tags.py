from django import template
register = template.Library()

@register.filter
def is_liked(post, user):
    return post.likes.filter(user=user).exists()
