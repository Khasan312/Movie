from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from main.models import FilmImage
from main.views import CategoryListView, FilmsViewSet, FilmImageView, CommentsView, RatingView, FavoriteViewSet, \
    CommentViewSet

router = DefaultRouter()
router.register('films', FilmsViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="MovieRoom",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/categories/', CategoryListView.as_view()),
    path('v1/api/add-image/', FilmImageView.as_view()),
    path('v1/api/account/', include('account.urls')),
    path('v1/api/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
    path('', schema_view.with_ui()),
    path('v1/api/films/<int:id>/comments/', CommentViewSet.as_view({'get': 'list'})),
    path('v1/api/films/<int:id>/rating/', RatingView.as_view()),
    path('v1/api/films/<int:id>/favorite/', FavoriteViewSet.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
