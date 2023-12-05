import openai
import os
import json
import urllib.request
import requests
from .models import Article
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_news_items(category="general", lang="en", country="us", max_items="1"):
    """
    Fetches news items from an external API.

    Args:
        category (str): The news category.
        lang (str): Language for the news items.
        country (str): Country for the news items.
        max_items (str): Maximum number of news items to fetch.

    Returns:
        list: A list of news items as dictionaries.
    """
    # Constructing the API URL with query parameters for category, language, country, and item limit
    apikey = os.getenv("NEWS_API_KEY")
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang={lang}&country={country}&max={max_items}&apikey={apikey}&expand=content"

    # Sending a request to the API and parsing the response
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

        # Looping through the fetched articles to add the category field
        for i in range(len(articles)):
            articles[i]['category'] = category
        return articles


def generate_image(prompt):
    """
    Generates an image URL using OpenAI's image generation API.

    Args:
        prompt (str): The prompt for generating the image.

    Returns:
        str: The URL of the generated image.
    """
    # Sending a request to OpenAI's image generation API with the provided prompt
    response = openai.Image.create(
        prompt=f"{prompt}",
        n=1,
        size="1024x1024"
    )
    # Extracting the image URL from the response
    image_url = response['data'][0]['url']
    return image_url


def chat_with_gpt3(title, content):
    """
    Interacts with OpenAI's GPT-3 model to generate a prompt for image generation.

    Args:
        title (str): The title of the article.
        content (str): The content of the article.

    Returns:
        str: The generated prompt from the assistant.
    """
    # Creating a chat completion request to OpenAI with the title and content of the article
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"""Generate image prompt for DALL-E for the following article. Do not add the words 'Image Prompt:' before the prompt:
                   Title: {title}
                   Content = {content}
                   """
            }
        ]
    )
    # Extracting the assistant's reply from the response
    assistant_reply = response['choices'][0]['message']['content']
    return assistant_reply


def save_image_from_url(model_instance, url):
    """
    Downloads an image from a URL and saves it to a model instance.

    Args:
        model_instance: The model instance to attach the image to.
        url (str): The URL of the image to download.

    This function is typically used to download and attach images to Article instances.
    """
    # Requesting the image from the provided URL
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    # Preparing the image for saving
    img_io = BytesIO()
    img.save(img_io, format='JPEG')

    # Retrieving the last article's ID for filename generation
    last_article = Article.objects.order_by('-id').first()
    if last_article is not None:
        last_article_id = last_article.id

    # Defining the filename for the image
    filename = f'{last_article_id}.jpg'

    # Saving the image to the model instance
    model_instance.image.save(filename, ContentFile(img_io.getvalue()), save=True)


def generate_articles(amount=2):
    """
    Generates a specified number of articles using external APIs and OpenAI.

    Args:
        amount (int): The number of articles to generate.

    This function fetches news items, generates prompts, creates images, and saves articles to the database.
    """
    # Fetching a specified number of news articles from an external news API
    articles = get_news_items(category='business', max_items=str(amount))
    for i in range(amount):
        # Generating a prompt using GPT-3 for each article
        prompt = chat_with_gpt3(title=articles[i]['title'], content=articles[i]['content'])

        # Generating an image URL based on the prompt
        image_url = generate_image(prompt)

        # Creating a new Article instance with the fetched data
        article = Article.objects.create(
            title=articles[i]['title'],
            description=articles[i]['description'],
            body=articles[i]['content'],
            source=articles[i]['source']['name'],
            category=articles[i]['category']
        )

        # Saving the generated image to the article
        save_image_from_url(article, image_url)

        # Refreshing the instance to reflect the newly saved image
        article.refresh_from_db()


generate_articles()
