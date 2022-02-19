from django.db.models import Count, Q
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Category, Film, FilmImage, Comment, Rating, Favorite


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # reply_count = SerializerMethodField()
    author = SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('content', )

    def get_author(self, obj):
        return obj.author.username

    def to_representation(self, instance):
        representation = super(CommentSerializer, self).to_representation(instance)
        representation['likes'] = instance.likes.count()
        action = self.context.get('action')
        # if action == 'list':
        representation['comments'] = instance.content

        # else:
        #     representation['comments'] = CommentSerializer(instance.parent.first(), many=True).data
        return representation


class FilmSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Film
        fields = ('id', 'title', 'category', 'author', 'created_at', 'text', 'fees_in_usa', 'fess_in_world', 'budget' )



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = FilmImageSerializer(instance.images.all(),
                                                       many=True, context=self.context).data
        return representation


class FilmImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
