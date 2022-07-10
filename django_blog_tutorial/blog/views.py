from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, PostCommentRating, PostRating, PostFav, PostComment
from .forms import CommentCreateForm
import json



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostRateView(LoginRequiredMixin, SingleObjectMixin, View):
    model = PostRating

    def get_object(self, queryset):
        post_rating_obj = super().get_object(queryset)
        return 
        



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html as default
    context_object_name = 'posts' # <model>_list as default
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            post_user_vote_list = PostRating.objects.filter(user=self.request.user)
            post_user_fav_list = PostFav.objects.filter(user=self.request.user, fav=1).values_list('post', flat=True)
        else:
            post_user_vote_list = None
            post_user_fav_list = None

        context.update({
            'posts_rating_list': PostRating.objects.all(),
            'post_user_vote_list': post_user_vote_list,
            'post_user_fav_list': post_user_fav_list
        })
        return context


@login_required
def post_rate(request):
    if request.method == 'POST':
        user = request.user
        json_data = json.loads(request.body)
        action = json_data['action']
        post = json_data['post_id']
        post = Post.objects.get(pk=post)
        if PostRating.objects.filter(user=user, post=post).exists():
            PostRating.objects.filter(user=user, post=post).update(action=action)
        else:
            PostRating.objects.create(user=user, post=post, action=action)
        return HttpResponse(request, content_type='text/plain', headers={'content': 'Yay'})
    if request.method == 'GET':
        post_id = request.headers['post-id']
        post = Post.objects.get(id=post_id)
        score = PostRating.objects.filter(post=post).first().get_rating()
        return HttpResponse(request, content_type='text/plain', headers={'score': score})


@login_required
def post_fav(request):
    if request.method == 'POST':
        user = request.user
        # try:
        #     # user_fav_list = request.COOKIES['user_fav_list'].replace('[', '').replace(']', '')
        #     user_fav_list = request.COOKIES.get('user_fav_list')
        #     print(user_fav_list, type(user_fav_list))
        #     # user_fav_list = user_fav_list.split(', ')
        #     # print(user_fav_list)
        # except: user_fav_list = list()

        json_data = json.loads(request.body)
        if json_data['fav'] == 'True':
            fav = 1
        else: fav = 0

        post = json_data['post_id']
        post = Post.objects.get(pk=post)

        user_fav_list = PostFav.objects.filter(user=user, fav=1).values_list('post', flat=True)

        if PostFav.objects.filter(user=user, post=post).exists():
            PostFav.objects.filter(user=user, post=post).update(fav=fav)
        else:
            PostFav.objects.create(user=user, post=post, fav=fav)

        response = HttpResponse(request, content_type='text/plain', headers={'content': 'Yay'})
        response.set_cookie('user_fav_list', list(user_fav_list))

        return response



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html as default
    context_object_name = 'posts' # <model>_list as default
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# class PostCommentListView(ListView):
#     model = PostComment
#     template_name = 'blog/post_detail_comment_list.html'
#     context_object_name = 'comments'
#     ordering = ['-date']
#     paginate_by = 7

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         if self.request.user.is_authenticated:
#             try:
#                 # comment_list = PostCommentRating.objects.filter(user=self.request.user, post=self.get_object())
#                 comment_list = PostCommentRating.objects.filter(comment__post=Post.objects.get(pk=self.kwargs.get('pk')), user=self.request.user)
#             except:
#                 comment_list = None

#             context.update({
#                 'form': CommentCreateForm(),
#                 'comment_user_vote_list': comment_list
#             })


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                # comment_list = PostCommentRating.objects.filter(user=self.request.user, post=self.get_object())
                comment_list = PostCommentRating.objects.filter(comment__post=self.get_object(), user=self.request.user)
            except:
                comment_list = None

            context.update({
                'form': CommentCreateForm(),
                'comment_user_vote_list': comment_list
            })

        try:
            comments = PostComment.objects.filter(post=self.get_object()).order_by('-date')
            comments_count = comments.count()
            paginator = Paginator(comments, 7)
            page_number = self.request.GET.get('page')
            page_comments = paginator.get_page(page_number)

        except:
            page_comments = None
            comments_count = None

        context.update({
            'post_comments': page_comments,
            'comments_count': comments_count
        })
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            comment_form = CommentCreateForm(request.POST)
            if comment_form.is_valid():
                self.object = self.get_object()
                comment_form.instance.user = request.user
                comment_form.instance.post = self.get_object()
                comment_form.save()
                return self.render_to_response(context=self.get_context_data())
            json_data = json.loads(request.body)
            if json_data['comment-id'] and json_data['comment-action']:
                comment = PostComment.objects.get(id=json_data['comment-id'])
                action = json_data['comment-action']
                
                comment_object = PostCommentRating.objects.update_or_create(comment=comment, user=request.user, defaults={'action': action})

                # if PostCommentRating.objects.filter(comment=comment, user=request.user).exists():
                #    comment_object = PostCommentRating.objects.filter(comment=comment, user=request.user)
                #    comment_object.update(action=action)
                # else:
                #    comment_object = PostCommentRating.objects.create(comment=comment, user=request.user, action=action)
                #    comment_object.save()

                return HttpResponse(request, content_type='text/plain', headers={'comment-score': comment_object[0].get_rating()})


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    success_message = "Post was published"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    success_message = 'Post was updated'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Post

    success_message = 'Post was deleted successfully'

    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
