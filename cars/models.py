from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    make = models.CharField(max_length=100)  # марка автомобиля
    model = models.CharField(max_length=100)  # модель автомобиля
    year = models.PositiveIntegerField()  # год выпуска
    description = models.TextField()  # описание автомобиля
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания
    updated_at = models.DateTimeField(auto_now=True)  # дата последнего обновления
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # внешний ключ на пользователя, который создал запись

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Comment(models.Model):
    content = models.TextField()  # содержание комментария
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания комментария
    car = models.ForeignKey(Car, related_name='comments', on_delete=models.CASCADE)  # внешний ключ на автомобиль
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # внешний ключ на пользователя (автора комментария)

    def __str__(self):
        return f"Comment by {self.author} on {self.car}"
