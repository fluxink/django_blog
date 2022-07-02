from django.shortcuts import render
from matplotlib.style import context


posts = [
    {
        'author': 'FluxInk',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': '2 July 2022'
    },
    {
        'author': 'CripsyWood',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': '2 July 2022'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
