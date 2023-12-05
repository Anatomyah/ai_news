from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LoginView, LogoutView

# URL patterns for template-based views.
urlpatterns = [
    # Home page URL, managed by the 'home' view.
    path('', views.home, name='home'),

    # URL for the user signup page, handled by SignUpView.
    path('user/signup', views.SignUpView.as_view(), name='signup'),

    # Account details page URL, handled by the 'account' view.
    path('user/account', views.account, name='account'),

    # Login page URL, using Django's built-in LoginView with custom settings.
    path('user/login', LoginView.as_view(template_name='newsapp/form.html',
                                         extra_context={'header': 'Welcome to Brainwash News!',
                                                        'legend': 'Enter login details:',
                                                        'login_form': True},
                                         redirect_authenticated_user=True), name='login'),

    # Logout URL, using Django's built-in LogoutView.
    path('user/logout', LogoutView.as_view(), name='logout'),

    # URL for creating a new article, handled by CreateArticle view.
    path('article/create_article', views.CreateArticle.as_view(), name='create_article'),

    # URLs for different news categories, handled by corresponding views.
    path('news/general_news', views.general_news, name='general_news'),
    path('news/health_news', views.health_news, name='health_news'),
    path('news/economic_news', views.economic_news, name='economic_news'),

    # Article editing URL, managed by UpdateArticle view.
    path('article/<int:pk>/edit/', views.UpdateArticle.as_view(), name='article_edit'),

    # Detail view for a specific article, handled by ArticleDetailView.
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_view'),

    # URL for deleting an article, managed by the 'article_delete' view.
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),

    # URL for requesting additional permissions, managed by the 'request_permission' view.
    path('user/request_permission', views.request_permission, name='req_perm'),

    # Test URL, handled by the 'test' view (presumably for development/testing purposes).
    path('test', views.test, name='test'),
]

# Including static file serving URLs for development purposes.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)