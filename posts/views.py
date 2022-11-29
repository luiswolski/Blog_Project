from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comments.forms import FormComment
from comments.models import Comment
from django.contrib import messages


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(published_post=True)
        qs = qs.annotate(
            num_comments = Count(
                Case(
                    When(comment__published_comment=True, then=1)
                )
            )
        )

        return qs


class PostSearch(PostIndex):
    template_name = 'posts/post_search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        word = self.request.GET.get('word')

        if not word:
            return qs

        qs = qs.filter(
            Q(title_post__icontains=word) |
            Q(author_post__first_name__iexact=word) |
            Q(content_post__icontains=word) |
            Q(excerpt_post__icontains=word) |
            Q(category_post__name_cat__iexact=word)
        )


        return qs


class PostCategory(PostIndex):
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('category_post')
        category = self.kwargs.get('category', None)

        if not category:
            return qs

        qs = qs.filter(category_post__name_cat__iexact=category)

        return qs


class PostDetails(UpdateView):
    template_name = 'posts/post_details.html'
    model = Post
    form_class = FormComment
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(published_comment=True, post_comment=post.id)

        context['comments'] = comments


        return context

    def form_valid(self, form):
        post = self.get_object()
        comment = Comment(**form.cleaned_data)
        comment.post_comment = post

        if self.request.user.is_authenticated:
            comment.user_comment = self.request.user

        comment.save()
        messages.success(self.request, 'Comment sent successfully')
        return redirect('post_details', pk=post.id)

