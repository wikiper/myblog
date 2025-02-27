import markdown
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like


def post_list(request):
    query = request.GET.get('q')
    if query:
        posts_received = Post.objects.filter(title__icontains=query)
    else:
        posts_received = Post.objects.all().order_by('-created_at')  # 按创建时间倒序排列
    paginator = Paginator(posts_received, 5)  # 每页显示 5 篇文章
    page_number = request.GET.get('page')  # 获取当前页码
    posts = paginator.get_page(page_number)
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.content = markdown.markdown(post.content)  # 将 Markdown 转换为 HTML
    comments = post.comments.all()  # 获取所有评论

    if request.method == 'POST':
        author = request.POST.get('author')
        content = request.POST.get('content')
        Comment.objects.create(post=post, author=author, content=content)
        return redirect('post_detail', post_id=post.id)

    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Like.objects.get_or_create(user=request.user, post=post)
    return redirect('post_detail', post_id=post.id)


@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})