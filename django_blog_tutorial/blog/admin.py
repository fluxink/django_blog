from django.contrib import admin
from .models import Post, PostComment, PostRating, PostFav


admin.site.register(Post)
admin.site.register(PostRating)
admin.site.register(PostFav)
admin.site.register(PostComment)
