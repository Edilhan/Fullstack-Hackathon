from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product, Category, Comment, Like, Rating, Favorite
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer
from .permissions import IsAuthor
from rest_framework.pagination import PageNumberPagination

class MyPaginationClass(PageNumberPagination):      #Здесь мы определяем свою пагинацию и отображение на странице всех продуктов
    page_size = 5

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            desc = data[i]['desc']
            data[i]['desc'] = desc[:15] + '...'
        return super().get_paginated_response(data)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # pagination_class = MyPaginationClass #Вставляем свою пагинацию

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('title', openapi.IN_QUERY, 'search auto by title', type=openapi.TYPE_STRING)])

    @action(methods=['GET'], detail=False)
    def search(self, request):
        name = request.query_params.get('title')
        queryset = self.get_queryset()
        if name:
            queryset = queryset.filter(title__icontains=name)
        
        serializer = ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, 200)
    
    # @action(methods=["GET"], detail=False)
    # def order_by_rating(self, request):
    #     queryset = self.get_queryset()

    #     queryset = sorted(queryset, key=lambda product: product.get_average_rating, reverse=True)
    #     serializer = ProductSerializer(queryset, many=True, context={"request":request})
    #     return Response(serializer.data, 200)

class CategoryViewSet(mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    mixins.ListModelMixin, 
                    GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     weeks_count

    # @api_view(["GET"])
    # def type(self, request):
    #     queryset = get_queryset
    #     queryset
    #     serializer = CategorySerializer(queryset, many=True)
    #     return Response(serializer.data, 200)

class CommentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

@api_view(["GET"])
def toggle_like(request, p_id):
    user = request.user
    product = get_object_or_404(Product, id=p_id)

    if Like.objects.filter(user=user, product=product).exists():
        Like.objects.filter(user=user, product=product).delete()
    else:
        Like.objects.create(user=user, product=product)
    return Response("Like toggled", 200)

@api_view(["POST"])
def add_rating(request, p_id):
    user = request.user
    product = get_object_or_404(Product, id=p_id)
    value = request.POST.get("value")

    if not user.is_authenticated:
        raise ValueError("authentication credentials are not provided")

    if not value:
        raise ValueError("value is required")
    
    if Rating.objects.filter(user=user, product=product).exists():
        rating = Rating.objects.get(user=user, product=product)
        rating.value = value
        rating.save()
    else:
        Rating.objects.create(user=user, product=product, value=value)
    
    return Response("rating created", 201)

@api_view(["GET"])
def add_to_favorites(request, r_id):
    user = request.user
    product = get_object_or_404(Product, id=r_id)

    if Favorite.objects.filter(user=user, product=product).exists():
        Favorite.objects.filter(user=user, product=product).delete()
    else:
        Favorite.objects.create(user=user, product=product)
    return Response("Added to favorites", 200)