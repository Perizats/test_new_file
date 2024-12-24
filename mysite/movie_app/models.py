from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


STATUS_CHOICES = (
    ('pro', 'pro'),
    ('simple', 'simple')
)

class Profile(AbstractUser):
    age = models.PositiveIntegerField(validators=[MinValueValidator(18),
                                                  MaxValueValidator(55)],
                                      null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Country(models.Model):
   country_name = models.CharField(max_length=32, unique=True)

   def __str__(self):
       return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=32)
    bio = models.TextField()
    age = models.PositiveIntegerField()
    director_image = models.ImageField(upload_to='director_images')

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=32)
    bio = models.TextField()
    age = models.PositiveIntegerField()
    actor_image = models.ImageField(upload_to='actor_images')

    def __str__(self):
        return self.actor_name

class Genre(models.Model):
    genre_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    country = models.ManyToManyField(Country, related_name='movies')
    director = models.ManyToManyField(Director, related_name='director_movies')
    actor = models.ManyToManyField(Actor, related_name='actor_movies')
    genre = models.ManyToManyField(Genre, related_name='genre_movies')
    TYPE_CHOICES = (
        ('144p', '144p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    )
    types = MultiSelectField(max_length=160, choices=TYPE_CHOICES, max_choices=5)
    movie_time = models.PositiveIntegerField( )
    description = models.TextField()
    movie_trailer = models.FileField(upload_to='movie_videos')
    movie_image = models.ImageField(upload_to='movie_poster')
    status_movie = models.CharField(max_length=16, choices=STATUS_CHOICES)

    def __str__(self):
        return self.movie_name


    def get_avg_rating(self):
        rating = self.ratings.all()
        if rating.exists():
            return round(sum(i.stars for i in rating) / rating.count(), 1)
        return 0


class MovieLanguages(models.Model):
    language = models.CharField(max_length=32)
    video = models.FileField(upload_to='movie_language')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_videos')

    def __str__(self):
        return self.language


class Moments(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_moments')
    movie_moments = models.ImageField(upload_to='moments')

class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.movie}'


class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.movie}'