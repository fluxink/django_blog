from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PostCommentRating, PostComment


@receiver(post_save, sender=PostCommentRating)
def save_comment_score(sender, instance, **kwargs):
    score = instance.get_rating()
    comment_obj = instance.comment
    comment_obj.score=score
    comment_obj.save()

