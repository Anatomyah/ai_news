from django.shortcuts import render, redirect
from .forms import *
from .utils import *
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from .templatetags.group_validate import user_in_group


@login_required()
def home(request):
    # Fetching the latest 5 articles ordered by publication time
    articles = Article.objects.order_by('-time_published')[:5]

    # Rendering the home template with the articles and a title context
    return render(request, template_name='home.html', context={'title': 'Home', 'articles': articles})


class SignUpView(generic.CreateView):
    # Django generic CreateView for user signup
    form_class = UserCreationForm  # Form class used for creating users
    success_url = reverse_lazy('login')  # Redirect to login upon successful signup
    template_name = 'form.html'  # Template for rendering the signup form

    def form_valid(self, form):
        # Method called when valid form data has been POSTed
        messages.success(self.request, 'User created successfully!')  # Display success message
        return super().form_valid(form)  # Call the parent class's form_valid method


@login_required()
def account(request):
    # Rendering the account template with the title context
    return render(request, template_name='account.html', context={'title': 'Account'})


class CreateArticle(CreateView):
    # Django generic CreateView for creating articles
    model = Article  # Model that the form is linked to
    form_class = ArticleForm  # Form class used for the article creation
    template_name = 'newsapp/form.html'  # Template for rendering the article creation form
    success_url = 'create_article'  # URL to redirect to on successful creation

    def form_valid(self, form):
        # Method called when valid form data has been POSTed
        messages.success(self.request,
                         f'Article {form.cleaned_data.get("title")} created successfully!')  # Display success message
        return super().form_valid(form)  # Call the parent class's form_valid method

    def get_context_data(self, **kwargs):
        # Method to insert additional context into the template
        context = super().get_context_data(**kwargs)  # Get existing context from the superclass
        context.update({
            'header': 'Create Article',
            'legend': 'Enter article details'
        })
        return context


class UpdateArticle(UpdateView):
    # Django generic UpdateView for updating articles
    model = Article  # Model that the form is linked to
    template_name = 'newsapp/form.html'  # Template for rendering the article update form

    def get_form_class(self):
        # Method to dynamically choose the form class based on user group
        base_form_class = ArticleForm  # Base form class for articles

        if user_in_group(user=self.request.user, group_name='Senior editors'):
            # If user belongs to 'Senior editors' group, use form with 'title' field
            class ArticleFormWithTitle(base_form_class):
                class Meta(base_form_class.Meta):
                    fields = ['title', 'body', 'image', 'writer', 'category']

            return ArticleFormWithTitle
        else:
            # Otherwise, use form without 'title' field
            class ArticleFormWithoutTitle(base_form_class):
                class Meta(base_form_class.Meta):
                    fields = ['body', 'image', 'writer', 'category']

            return ArticleFormWithoutTitle

    def form_valid(self, form):
        # Method called when valid form data has been POSTed
        response = super().form_valid(form)  # Call the parent class's form_valid method
        messages.success(self.request, f'Article "{self.object.title}" edited successfully!')  # Display success message
        edit_url = self.request.COOKIES.get('edit_url', reverse('general_news'))  # Retrieve or set the success URL
        self.success_url = edit_url
        return response

    def get_context_data(self, **kwargs):
        # Method to insert additional context into the template
        context = super().get_context_data(**kwargs)  # Get existing context from the superclass
        context.update({
            'header': f'Article {self.object.title}',
            'legend': 'Edit article details'
        })
        return context


@login_required()
def general_news(request):
    # Fetching general news articles ordered by publication time
    articles = Article.objects.filter(category='gen').order_by('-time_published')[:5]

    # Rendering the newspage template with the articles and title context
    return render(request, template_name='newspage.html',
                  context={'title': 'General News', 'articles': articles, 'header': 'General News'})


# Similarly, health_news and economic_news views are defined with respective category filters
@login_required()
def health_news(request):
    articles = Article.objects.filter(category='hel').order_by('-time_published')[:5]

    return render(request, template_name='newspage.html', context={'title': 'General News',
                                                                   'articles': articles,
                                                                   'header': 'Health News'})


# Similarly, health_news and economic_news views are defined with respective category filters
@login_required()
def economic_news(request):
    articles = Article.objects.filter(category='eco').order_by('-time_published')[:5]

    return render(request, template_name='newspage.html', context={'title': 'General News',
                                                                   'articles': articles,
                                                                   'header': 'Economics News'})


class ArticleDetailView(DetailView):
    # Django generic DetailView for displaying an article
    model = Article  # Model that the detail view is linked to
    template_name = 'newsapp/article.html'  # Template for rendering the article detail

    def render_to_response(self, context, **response_kwargs):
        # Method called to render the response
        response = super().render_to_response(context, **response_kwargs)  # Call the parent class's method
        response.set_cookie('edit_url', self.request.build_absolute_uri())  # Set a cookie with the current URL
        return response


@login_required()
def article_delete(request, pk):
    # Fetching the article by primary key
    article = Article.objects.get(id=pk)
    if article:  # Check if the article exists
        article.delete()  # Delete the article
        messages.success(request, f'Article "{article.title}" deleted successfully!')  # Display success message
        return redirect('general_news')  # Redirect to the general news page


def add_permissions(user, permission_list):
    """
    Add permissions to a user.

    :param user: User instance to which permissions will be added
    :param permission_list: List of permission strings (e.g., ["app_label.permission_codename", ...])
    """
    # Fetch permission objects based on the provided list
    permissions = Permission.objects.filter(codename__in=permission_list)

    # Add permissions to the user
    for perm in permissions:
        user.user_permissions.add(perm)


@login_required()
def request_permission(request):
    if request.method == 'GET':
        # Render the form template for GET requests
        return render(request, template_name='form.html', context={'title': 'Request Permission', 'form': PermissionRequestForm, 'url': reverse('req_perm'), 'header': 'Request Permission', 'legend': 'Choose the relevant permissions:'})

    if request.method == 'POST':
        # Handle form submission for POST requests
        form = PermissionRequestForm(request.POST)
        if form.is_valid():  # Check if the form data is valid
            # Create a permission request and grant permissions
            permission_request = PermissionRequest.objects.create(user=request.user)
            permission_request.permissions.set(form.cleaned_data['permissions'])
            permission_request.save()
            add_permissions(request.user, form.cleaned_data['permissions'])
            messages.success(request, f'Permissions granted successfully!')

            return redirect('account')  # Redirect to the account page
        else:
            # Re-render the form with validation errors
            return render(request, template_name='form.html', context={'title': 'Request Permission', 'form': form, 'url': reverse('req_perm'), 'header': 'Request Permission', 'legend': 'Choose the relevant permissions:'})
