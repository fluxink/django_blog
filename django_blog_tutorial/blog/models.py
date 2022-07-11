from email.policy import default
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce import models as tinymce_models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = tinymce_models.HTMLField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class PostRating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20)

    def get_rating(self):
        likes = PostRating.objects.filter(post=self.post, action='like').count()
        dislikes = PostRating.objects.filter(post=self.post, action='dislike').count()
        return likes - dislikes

    def __str__(self):
        return f'{self.user} {self.action} {self.post}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_combination')
        ]


class PostFav(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fav = models.BooleanField()

    def __str__(self):
        return f'{self.user} fav "{self.post}"'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_combination_fav')
        ]


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} comment "{self.post}"'


class PostCommentRating(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20)

    def get_rating(self):
        likes = PostCommentRating.objects.filter(comment=self.comment, action='like').count()
        dislikes = PostCommentRating.objects.filter(comment=self.comment, action='dislike').count()
        return likes - dislikes

    def __str__(self):
        return f'{self.user} {self.action} comment-id: {self.comment.id}'


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_user_comment_combination')
        ]
