from rest_framework.decorators import api_view
from rest_framework.response import Response
from newsapp.models import Article, Source, ContactMessage
from .serializers import ArticleSerializer, SourceSerializer, ContactMessageSerializer
from rest_framework import status


@api_view(['GET', 'POST', 'PUT'])
def get_article(request):
    """
    API view for handling requests related to the Article model.

    Supports GET, POST, and PUT HTTP methods.

    GET: Fetches one or all articles based on the presence of an 'id' parameter.
    POST: Creates a new article using the provided data.
    PUT: Updates an existing article identified by an 'id' parameter.

    Args:
        request: The incoming HTTP request.

    Returns:
        Response: Contains the serialized data or an error message.
    """

    # Handling GET requests to either fetch a specific article or all articles.
    if request.method == 'GET':
        article_id = request.query_params.get('id', False)
        if not article_id:
            articles = Article.objects.all()
            res = ArticleSerializer(articles, many=True)
        else:
            article = Article.objects.get(pk=article_id)
            res = ArticleSerializer(instance=article)
        return Response(res.data)

    # Handling POST requests to create a new article.
    elif request.method == 'POST':
        article_ser = ArticleSerializer(data=request.data)
        if article_ser.is_valid():
            article_ser.save()
            return Response("Article created successfully")
        else:
            return Response({'error': article_ser.errors})

    # Handling PUT requests to update an existing article.
    elif request.method == 'PUT':
        article_id = request.query_params.get('id', False)
        article = Article.objects.get(pk=article_id)
        article_ser = ArticleSerializer(instance=article, data=request.data)
        if article_ser.is_valid():
            article_ser.save()
            return Response("Article updated successfully")
        else:
            return Response({'error': article_ser.errors})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def get_message(request):
    """
    API view for handling requests related to the ContactMessage model.

    Supports GET, POST, PUT, and DELETE HTTP methods.

    GET: Fetches one or all contact messages based on the presence of an 'id' parameter.
    POST: Creates a new contact message using the provided data.
    PUT: Updates an existing contact message identified by an 'id' parameter.
    DELETE: Deletes an existing contact message identified by an 'id' parameter.

    Args:
        request: The incoming HTTP request.

    Returns:
        Response: Contains the serialized data or an error message.
    """

    # Handling GET, POST, PUT, DELETE methods for ContactMessage model.
    # Each method's implementation includes fetching, creating, updating, or deleting contact messages.
    if request.method == 'GET':
        source_id = request.query_params.get('id', False)
        if not source_id:
            articles = Source.objects.order_by('-time_published')[:5]
            res = SourceSerializer(articles, many=True)
        else:
            source = Source.objects.get(pk=source_id)
            res = SourceSerializer(instance=source)
        return Response(res.data)

    elif request.method == 'POST':
        source_ser = SourceSerializer(data=request.data)
        if source_ser.is_valid():
            source_ser.save()
            return Response({'status': 'OK', 'info': 'Source added'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'info': source_ser.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        source_id = request.query_params.get('id', False)
        if not source_id:
            return Response({'status': 'error', 'info': 'ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            source = Source.objects.get(pk=source_id)
            source_ser = SourceSerializer(instance=source, data=request.data, partial=True)
            if source_ser.is_valid():
                source_ser.save()
                return Response({'status': 'OK', 'info': 'Source updated'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'info': source_ser.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        source_id = request.query_params.get('id', False)
        if not source_id:
            return Response({'status': 'error', 'info': 'ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            source = Source.objects.get(pk=source_id)
            if source():
                source.delete()
                return Response({'status': 'OK', 'info': 'Source deleted'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'info': source.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def get_message(request):
    if request.method == 'GET':
        message_id = request.query_params.get('id', False)
        if not message_id:
            articles = ContactMessage.objects.all()
            res = ContactMessageSerializer(articles, many=True)
        else:
            message = ContactMessage.objects.get(pk=message_id)
            res = ContactMessageSerializer(instance=message)
        return Response(res.data)

    elif request.method == 'POST':
        message_ser = ContactMessageSerializer(data=request.data)
        if message_ser.is_valid():
            message_ser.save()
            return Response({'status': 'OK', 'info': 'Message added'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'info': message_ser.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        message_id = request.data.get('id', False)
        if not message_id:
            return Response({'status': 'error', 'info': 'ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = ContactMessage.objects.get(pk=message_id)
            message_ser = ContactMessageSerializer(instance=message, data=request.data, partial=True)
            if message_ser.is_valid():
                message_ser.save()
                return Response({'status': 'OK', 'info': 'Message updated'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'info': message_ser.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        message_id = request.data.get('id', False)
        if not message_id:
            return Response({'status': 'error', 'info': 'ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = ContactMessage.objects.get(pk=message_id)
            if message:
                message.delete()
                return Response({'status': 'OK', 'info': 'Message deleted'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'info': message.errors}, status=status.HTTP_400_BAD_REQUEST)
