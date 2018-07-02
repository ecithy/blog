from django.conf.urls import url
from .views import index, do_reg, do_login, do_logout, ArticleDetail, AddComentsView

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^reg$', do_reg, name='reg'),
    url(r'^login$', do_login, name='login'),
    url(r'^logout$', do_logout, name='logout'),

    url(r'^article_detail/(?P<article_id>\d+)$', ArticleDetail.as_view(), name='article_detail'),

    # 添加课程评论
    url(r'^add_comment/(?P<article_id>\d+)$', AddComentsView.as_view(), name="add_comment"),
]
