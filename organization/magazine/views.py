from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView

from organization.magazine.models import Article
from organization.core.views import SlugMixin

# Create your views here.
class ArticleDetailView(SlugMixin, DetailView):

    model = Article
    template_name='magazine/article/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        return context

class ArticleListView(SlugMixin, ListView):

    model = Article
    template_name='magazine/article/article_list.html'
    # context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        return context


# def blog_post_detail(request, slug, year=None, month=None, day=None,
#                      template="blog/blog_post_detail.html",
#                      extra_context=None):
#     """. Custom templates are checked for using the name
#     ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
#     posts's slug.
#     """
#     blog_posts = BlogPost.objects.published(
#                                      for_user=request.user).select_related()
#     blog_post = get_object_or_404(blog_posts, slug=slug)
#     related_posts = blog_post.related_posts.published(for_user=request.user)
#     context = {"blog_post": blog_post, "editable_obj": blog_post,
#                "related_posts": related_posts}
#     context.update(extra_context or {})
#     templates = [u"blog/blog_post_detail_%s.html" % str(slug), template]
#     return TemplateResponse(request, templates, context)
