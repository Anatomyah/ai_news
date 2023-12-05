from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User, Permission


class ContactMessage(models.Model):
    """
    Model representing a contact message in the system.

    Attributes:
        name (CharField): The name of the sender.
        email (CharField): The email address of the sender.
        title (CharField): The title or subject of the message.
        content (CharField): The body of the message.
    """
    # Fields definition
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=250)


class Source(models.Model):
    """
    Model representing a news source.

    Attributes:
        name (CharField): The name of the news source.
        url (CharField): The URL of the news source's website.
    """
    # Fields definition
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)


class Article(models.Model):
    """
    Model representing an article.

    Attributes:
        title (CharField): The title of the article.
        description (CharField): A brief description of the article.
        image (ImageField): An optional image for the article.
        body (CharField): The main content of the article.
        source (CharField): The source of the article.
        category (CharField): The category of the article (e.g., General, World, etc.).
        time_published (DateTimeField): The publication time of the article.
        site (ForeignKey): A foreign key linking to the Source model.

    Methods:
        get_absolute_url: Returns the URL for the article's detail view.
    """
    # Fields definition and Meta class with custom permissions
    CATEGORIES = [
        ('general', 'General'),
        ('world', 'World'),
        ('nation', 'Nation'),
        ('business', 'Business'),
        ('technology', 'Technology'),
        ('entertainment', 'Entertainment'),
        ('sports', 'Sports'),
        ('science', 'Science'),
        ('health', 'Health'),
    ]

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, default=1)
    image = models.ImageField(upload_to='images/', null=True)
    body = models.CharField(max_length=5000)
    source = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='gen')
    time_published = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(to=Source, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('article_view', args=[self.pk])

    class Meta:
        permissions = [
            ("edit_title", "Can edit article titles"),
        ]


class PermissionRequest(models.Model):
    """
    Model representing a request for user permissions.

    Attributes:
        user (ForeignKey): A foreign key linking to the User model.
        permissions (ManyToManyField): Many-to-many field linking to the Permission model.
    """
    # Fields definition
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    permissions = models.ManyToManyField(Permission)
