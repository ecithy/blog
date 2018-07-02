from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *


# Create your views here.

# 分页代码
def getPage(request, article_list):
    # 每页2条
    paginator = Paginator(article_list, 2)
    try:
        # 用户没有传值，默认page为1
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        # 出异常默认显示第一页
        article_list = paginator.page(1)
    return article_list


# 首页
def index(request):
    article_list = Article.objects.all()
    article_list = getPage(request, article_list)
    return render(request, 'index.html', locals())


# 注册
def do_reg(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            # 注册
            user = User.objects.create(username=reg_form.cleaned_data["username"],
                                       # email=reg_form.cleaned_data["email"],
                                       password=make_password(reg_form.cleaned_data["password"]), )
            user.save()

            # 登录
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'failure.html', {'reason': reg_form.errors})
    else:
        reg_form = RegForm()

    return render(request, 'reg.html', locals())


# 登录
def do_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 登录
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return render(request, 'failure.html', {'reason': '登录验证失败'})
        else:
            return render(request, 'failure.html', {'reason': login_form.errors})
    else:
        login_form = LoginForm()

    return render(request, 'login.html', locals())


# 注销
def do_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse("index"))


# 文章详情页
class ArticleDetail(View):
    def get(self, request, article_id):
        article_id = int(article_id)
        all_article = Article.objects.all()
        all_count = all_article.count()
        article = Article.objects.get(id=article_id)

        # 判断上一页或下一页是否存在
        try:
            before_page_article = Article.objects.get(id=article_id + 1)
            after_page_article = Article.objects.get(id=article_id - 1)
        except Exception:  # 不存在则返回一个变量article_not_exsist
            article_not_exsist = True
            if article_id == all_count:
                after_page_article = Article.objects.get(id=article_id - 1)
            if article_id == 1:
                before_page_article = Article.objects.get(id=article_id + 1)

        return render(request, 'article-detail.html', locals())


# 文章评论
class AddComentsView(View):
    def post(self, request, article_id):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        article_id = int(request.POST.get("article_id", 0))
        comments = request.POST.get("comments", "")
        if article_id > 0 and comments:
            article_comments = Comment()
            article = Article.objects.get(id=int(article_id))

            article_comments.article = article
            article_comments.content = comments
            article_comments.user = request.user
            article_comments.us
            article_comments.save()
            print(article_comments.user)
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')