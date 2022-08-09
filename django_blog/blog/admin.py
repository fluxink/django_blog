from django.contrib import admin
from .models import Post, PostComment, PostCommentRating, PostRating, PostFav


admin.site.register(Post)
admin.site.register(PostRating)
admin.site.register(PostFav)
admin.site.register(PostComment)
admin.site.register(PostCommentRating)
