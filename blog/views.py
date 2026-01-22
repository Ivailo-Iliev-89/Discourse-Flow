from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Comment, Tag
from .forms import CommentForm, PostForm
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms


# Views of Base logic

# --------------------------
# Post List #
# --------------------------

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        """Return only a published posts"""

        return Post.objects.filter(
            status=Post.PUBLISHED).exclude(slug__exact='').select_related('author').prefetch_related('tags')


# --------------------------
# Post Detail + Comments
# --------------------------

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(status=Post.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        context['comments'] = post.comments.filter(active=True, parent__isnull=True)
        context['comment_form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        """Post Details for comments"""

        self.object = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = self.object

            if request.user.is_authenticated:
                new_comment.user = request.user

            # Reply Logic
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    new_comment.parent = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    pass

            new_comment.save()
            return redirect(self.object.get_absolute_url())

        context = self.get_context_data()
        context['comment_form'] = comment_form

        return self.render_to_response(context)


# --------------------------
# Post Create
# --------------------------

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('blog:post_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tags'].widget = forms.CheckboxSelectMultiple()
        form.fields['tags'].queryset = Tag.objects.all()

        for field_name, field in form.fields.items():
            if field_name != 'tags':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input-group'})

        if 'category' in form.fields:
            form.fields['category'].empty_label = "Select Category"

        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'P'
        return super().form_valid(form)


# --------------------------#
# Post Update
# --------------------------#

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'content', 'image', 'category', 'tags']
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tags'].widget = forms.CheckboxSelectMultiple()

        for field_name, field in form.fields.items():
            if field_name != 'tags':
                field.widget.attrs.update({'class': 'form-control'})

        if 'category' in form.fields:
            form.fields['category'].empty_label = "Select Category"

        return form

    def test_func(self):
        """"Only the creator of the post can edit"""
        post = self.get_object()
        return post.author == self.request.user


# --------------------------#
# Post Delete
# --------------------------#

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        """Only the creator of the post can delete"""
        post = self.get_object()
        return post.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        """After deleting , we are going back into the same article"""
        return self.object.post.get_absolute_url()

    def test_func(self):
        """Checking if this user is author of the comment"""
        comment = self.get_object()
        return self.request.user == comment.user
