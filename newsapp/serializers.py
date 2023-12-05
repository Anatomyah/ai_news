from rest_framework import serializers
from .models import Article, Source, ContactMessage


class ArticleMiniSerializer(serializers.ModelSerializer):
    """
    A minimal serializer for the Article model, focusing on specific fields.

    This serializer is typically used for nested serialization within another serializer.

    Meta:
        model: Specifies the Article model as the source of serialization.
        fields: Defines 'title' as the field to be serialized.
    """
    # Meta class definition
    class Meta:
        model = Article
        fields = ('title',)


class SourceMiniSerializer(serializers.ModelSerializer):
    """
    A serializer for the Source model with nested ArticleMiniSerializer.

    This serializer includes related Article instances as nested data.

    Meta:
        model: Specifies the Source model as the source of serialization.
        fields: Includes 'name' and nested articles.
    """
    article_set = ArticleMiniSerializer(many=True)
    # Meta class definition
    class Meta:
        model = Source
        fields = ('name',)


class ArticleSerializer(serializers.ModelSerializer):
    """
    A comprehensive serializer for the Article model.

    This serializer handles all fields of the Article model and includes a nested SourceMiniSerializer.

    Meta:
        model: Specifies the Article model as the source of serialization.
        fields: Includes all fields of the Article model.
    """
    site_id = serializers.IntegerField()
    site = SourceMiniSerializer(read_only=True)
    # Meta class definition
    class Meta:
        model = Article
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    """
      A basic serializer for the Source model.

      Meta:
          model: Specifies the Source model as the source of serialization.
          fields: Includes 'name' as the field to be serialized.
      """

    # Meta class definition
    class Meta:
        model = Source
        fields = ("name",)


class ContactMessageSerializer(serializers.ModelSerializer):
    """
      A comprehensive serializer for the ContactMessage model.

      Meta:
          model: Specifies the ContactMessage model as the source of serialization.
          fields: Includes all fields of the ContactMessage model.
      """

    # Meta class definition
    class Meta:
        model = ContactMessage
        fields = '__all__'


class ContactMessageMiniSerializer(serializers.ModelSerializer):
    """
       A minimal serializer for the ContactMessage model.

       Meta:
           model: Specifies the ContactMessage model as the source of serialization.
           fields: Includes 'name' as the field to be serialized.
       """

    # Meta class definition
    class Meta:
        model = ContactMessage
        fields = ('name',)


