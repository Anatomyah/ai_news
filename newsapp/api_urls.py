from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import api_views

# URL patterns for the API endpoints.
urlpatterns = [
    # Defines a URL path for fetching articles. The 'get_article' view handles requests at this endpoint.
    path('article', api_views.get_article, name='article'),

    # URL path for fetching source data. Handled by the 'get_source' view.
    path('source', api_views.get_source, name='source'),

    # Endpoint for fetching messages, managed by the 'get_message' view.
    path('message', api_views.get_message, name='message'),
]

# Appends static file serving URLs to the URL patterns, allowing media files to be served in development.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)