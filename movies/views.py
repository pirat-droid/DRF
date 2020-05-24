from django.db import models
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Actor
from .serilalizers import (MovieListSerializer,
                           MovieDetailSerializer,
                           ReviewCreateSerializer,
                           CreateRatingSerealizer,
                           ActorListSerializer,
                           ActorDetailSerializer,
                           )
from .service import get_client_ip, MovieFilter

class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


        # class MovieListView(APIView):
        #     """Вывод списка фильмов"""
        #     def get(self, request):
        #         movies = Movie.objects.filter(draft=False).annotate(
        # rating_user=models.Case(
        #     models.When(ratings__ip=get_client_ip(request), then=True),
        #     default=False,
        #     output_field=models.BooleanField()
        # ),
        #     rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
        # ).annotate(
        #     middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        # )
        # serializer = MovieListSerializer(movies, many=True)
        # return Response(serializer.data)
# class MovieDetailView(APIView):
#     """Вывод описания фильма"""
#     def get(self, request, pk):
#         movie = Movie.objects.get(id=pk, draft=False)
#         serializer = MovieDetailSerializer(movie)
#         return Response(serializer.data)


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод описания фильма"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer

# class ReviewCreaterView(APIView):
#     """Добавление озыва"""
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)

class ReviewCreaterView(generics.CreateAPIView):
    """Добавление озыва"""
    serializer_class = ReviewCreateSerializer

# class AddStarRatingView(APIView):
#     """Добавление рейтинга фильму"""
#     def post(self, request):
#         serializer = CreateRatingSerealizer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)

class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerealizer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

class ActorListView(generics.ListAPIView):
    """Вывод списка актёров и режисёров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

class ActorDetailView(generics.RetrieveAPIView):
    """Вывод полного описания актёра или режисёра"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer