from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
# import form
from .forms import PostForm

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    print(request.user)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    # sendwhatmsg_instantly('+254707438654','Hello from pywhatkit')
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# get the new blog form

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    # get post by id
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html',{'posts':posts})

@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_list')

@login_required
def unpublish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.unpublish()
    return redirect('post_draft_list')

@login_required
def delete_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')