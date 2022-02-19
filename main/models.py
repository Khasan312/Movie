from django.core.validators import MaxValueValidator
from django.db import models

from Blog_api import settings
from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Film(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='films')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='films')
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    budget = models.PositiveIntegerField("Бюджет", default=0,
                                         help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    favorites = models.ManyToManyField("Favorite", related_name='favorites', default=None, blank=True)

    def __str__(self):
        return self.title


class FilmImage(models.Model):
    image = models.ImageField(upload_to='films', blank=True, null=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(MyUser,
                                   related_name='likers',
                                   blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.id}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Rating(models.Model):
    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        unique_together = ['user', 'product']
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='product')
    rating = models.PositiveIntegerField(null=False, blank=False)

    # def __str__(self):
    #     return f'{self.product.id}'


class Favorite(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
