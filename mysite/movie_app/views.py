from rest_framework import viewsets, generics, permissions, status
from .serializers import *
from .models import *
from .permissions import CheckStatus, CheckUserRating
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import GenrePagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers

    def get_queryset(self):
        return  Profile.objects.filter(id=self.request.user.id)
    permission_classes = [permissions.IsAuthenticated]


class ProfileEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    permission_classes = [permissions.IsAuthenticated, CheckStatus]

    def get_queryset(self):
        return  Profile.objects.filter(id=self.request.user.id)


class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = Country
    permission_classes = [permissions.IsAuthenticated]


class CountryDetailAPIView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializers
    permission_classes = [permissions.IsAuthenticated]


class ActorListAPIView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializers
    permission_classes = [permissions.IsAuthenticated]


class ActorDetailAPIView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializers
    permission_classes = [permissions.IsAuthenticated]


class DirectorListAPIView(generics.RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializers
    permission_classes = [permissions.IsAuthenticated]


class DirectorDetailAPIView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorDetailSerializers
    permission_classes = [permissions.IsAuthenticated]


class GenreListAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = GenrePagination


class GenreDetailAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreDetailSerializers
    permission_classes = [permissions.IsAuthenticated]


class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter , OrderingFilter]
    filter_fields = ['country', 'genre']
    search_fields = ['movie_name']
    ordering_fields = ['movie_name', 'year']


class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializers


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers
    permission_classes = [CheckUserRating]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMovie.objects.all()
    serializer_class = FavoriteItemSerializers


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializers

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)
