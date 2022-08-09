from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PostCommentRating, PostComment, PostRating


@receiver(post_save, sender=PostCommentRating)
def save_comment_score(sender, instance, **kwargs):
    score = instance.get_rating()
    comment_obj = instance.comment
    comment_obj.score=score
    comment_obj.save()

@receiver(post_save, sender=PostRating)
def save_post_score(sender, instance, **kwargs):
    score = instance.get_rating()
    post_obj = instance.post
    post_obj.score=score
    post_obj.save()
    
