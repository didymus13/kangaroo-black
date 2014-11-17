from django.shortcuts import render, get_object_or_404
from campaignManager.blog.models import Post
import datetime

def home(request):
    return render(request, 'home.html', {
        'user': request.user,
        'posts': Post.objects.filter(live_date__lte = datetime.datetime.now())
    })
    
def detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    
    return render(request, 'post.html', {
        'user': request.user,
        'post': post
    })
