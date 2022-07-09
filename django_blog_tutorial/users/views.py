import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.core.paginator import Paginator
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, MyAuthenticationForm
from .models import Profile
from blog.models import Post, PostComment, PostFav


class MyLoginView(LoginView):

    authentication_form = MyAuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created. Now you able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', { 'form': form, 'title': 'Create Account' })


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile-settings.html', context)


class UserDetailView(DetailView):

    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_obj = self.get_object().user
        
        posts = Post.objects.filter(author=user_obj).order_by('-date_posted')
        count_of_posts = posts.count()
        count_of_comments = PostComment.objects.filter(user=user_obj).count()

        if self.request.GET.get('favs') is not None:
            display_object = 'favs'
            try:
                # favs = PostFav.objects.filter(user=user_obj, fav=1).prefetch_related('post')
                favs = Post.objects.filter(postfav__user=user_obj, postfav__fav=1).order_by('-date_posted')
                paginator = Paginator(favs, 7)
                page_number = self.request.GET.get('favs')
                page_objects = paginator.get_page(page_number)
            except:
                page_objects = None
        else:
            display_object = 'posts'
            try:
                paginator = Paginator(posts, 7)
                page_number = self.request.GET.get('page')
                page_objects = paginator.get_page(page_number)
            except:
                page_objects = posts


        context.update({
            'count_of_posts': count_of_posts,
            'count_of_comments': count_of_comments,
            'page_objects': page_objects,
            'page_number': paginator.num_pages,
            'display_object': display_object
        })

        return context
    
