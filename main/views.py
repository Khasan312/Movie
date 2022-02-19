from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework.views import APIView
from django_filters.rest_framework import  DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from .models import Category, Film, Comment, Rating, Favorite
from main.serializers import CategorySerializer, FilmSerializer, FilmImageSerializer, CommentSerializer, \
    RatingSerializer, FavoriteSerializer
from rest_framework import generics, status
from rest_framework import viewsets
from .permissions import IsPostAuthor, IsAuthorPermission
from .service import PaginationFilms


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class FilmsViewSet(PermissionMixin, ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = PaginationFilms
    authentication_classes = [BasicAuthentication]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = FilmSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = FilmSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=True, methods=['get'])
    def like(self, request, pk):
        user = request.user
        reply = get_object_or_404(Comment, pk=pk)
        if user.is_authenticated:
            if user in reply.likes.all():
                reply.likes.remove(user)
                message = 'Unliked'
            else:
                reply.likes.add(user)
                message = 'Liked'
        context = {'Status': message}
        return Response(context, status=200)


class FilmImageView(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        print(self.kwargs['id'])
        return Comment.objects.filter(film_id=self.kwargs['id'])


class RatingView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        film_id = self.kwargs['id']
        queryset = queryset.filter(product=film_id)
        return queryset


class FavoriteViewSet(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


    def post(request, id):
        film = get_object_or_404(Film, slug=request.data.get('slug'))
        if request.user not in film.favourite.all():
            film.favourite.add(request.user)
            return Response({'detail': 'User added to post'}, status=status.HTTP_200_OK)
        return Response({'detail': 'dont'}, status=status.HTTP_400_BAD_REQUEST)







#
# class FileUploadView(views.APIView):
#     parser_classes = (FileUploadParser,)
#
#     def put(self, request, filename, format=None):
#         file_obj = request.data['file']
#         # ...
#         # do some stuff with uploaded file
#         # ...
#         return Response(status=204)