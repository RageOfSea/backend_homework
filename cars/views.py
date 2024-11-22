from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Car, Comment
from .forms import CarForm, CommentForm
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CarSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from .serializers import UserSerializer

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CarListView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]  # Только аутентифицированные пользователи могут создавать

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Присваиваем владельца

class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Этот метод фильтрует доступные автомобили так, чтобы пользователи могли
        редактировать только свои автомобили.
        """
        return Car.objects.filter(owner=self.request.user)



# Главная страница — Список всех автомобилей
def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})

# Страница с информацией о конкретном автомобиле и комментариями
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    comments = car.comments.all()  # Получаем все комментарии к автомобилю
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.car = car
            comment.author = request.user
            comment.save()
            return redirect('car_detail', car_id=car.id)  # Перезагружаем страницу с новым комментарием
    else:
        comment_form = CommentForm()

    return render(request, 'cars/car_detail.html', {'car': car, 'comments': comments, 'comment_form': comment_form})

# Форма для добавления нового автомобиля
@login_required
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user  # Назначаем владельца автомобиля
            car.save()
            return redirect('car_list')  # Перенаправляем на главную страницу
    else:
        form = CarForm()

    return render(request, 'cars/car_form.html', {'form': form})

# Форма для редактирования автомобиля
@login_required
def car_edit(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:  # Только владелец может редактировать
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)

    return render(request, 'cars/car_form.html', {'form': form})

# Удаление автомобиля
@login_required
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:  # Только владелец может удалять
        return HttpResponseForbidden()

    if request.method == 'POST':
        car.delete()
        return redirect('car_list')

    return render(request, 'cars/car_confirm_delete.html', {'car': car})


# Получить список автомобилей
class CarListView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Только авторизованные пользователи могут добавлять

    def perform_create(self, serializer):
        # Присваиваем владельца автомобиля текущему пользователю
        serializer.save(owner=self.request.user)

# Получить информацию о конкретном автомобиле
class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        car = self.get_object()
        if car.owner != self.request.user:
            raise PermissionDenied("Вы не можете редактировать этот автомобиль.")
        serializer.save()

# Получить список комментариев к автомобилю
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        car = self.get_car()
        return car.comments.all()

    def get_car(self):
        car_id = self.kwargs['car_id']
        return get_object_or_404(Car, id=car_id)

    def perform_create(self, serializer):
        car = self.get_car()
        serializer.save(car=car, author=self.request.user)

# Получить информацию о комментарии
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
