from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from moykotel.models import PostCategory
from moykotel.tasks.basic import new_posts_subscrition


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_posts_subscrition(instance)
