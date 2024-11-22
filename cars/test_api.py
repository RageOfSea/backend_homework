from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from cars.models import Car, Comment


class CarApiTestCase(TestCase):

    def setUp(self):
        """Подготовка тестовых данных: создание пользователя и автомобиля."""
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем тестовый автомобиль
        self.car = Car.objects.create(
            make="Toyota",
            model="Camry",
            year=2021,
            description="Компактный седан с хорошей экономией топлива",
            owner=self.user
        )

        # Создаем тестовый комментарий
        self.comment = Comment.objects.create(
            content="Отличный автомобиль!",
            car=self.car,
            author=self.user
        )

        # Инициализируем тестовый клиент
        self.client = APIClient()

        # Получаем JWT токен
        self.token = self.get_jwt_token()

    def get_jwt_token(self):
        """Получаем JWT токен для аутентифицированного пользователя."""
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_get_cars(self):
        """Тест на получение списка автомобилей"""
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['make'], 'Toyota')
        self.assertEqual(response.data[0]['model'], 'Camry')

    def test_get_car(self):
        """Тест на получение информации о конкретном автомобиле"""
        response = self.client.get(f'/api/cars/{self.car.id}/')  # Внимание, здесь car_id в URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['make'], 'Toyota')
        self.assertEqual(response.data['model'], 'Camry')

    def test_create_car_authenticated(self):
        """Тест на создание нового автомобиля для аутентифицированного пользователя"""
        self.client.credentials(Authorization='Bearer ' + self.token)
        data = {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2020,
            'description': 'Экономичный автомобиль'
        }
        response = self.client.post('/api/cars/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['make'], 'Honda')
        self.assertEqual(response.data['model'], 'Civic')

    def test_create_car_unauthenticated(self):
        """Тест на создание автомобиля для неаутентифицированного пользователя"""
        data = {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2020,
            'description': 'Экономичный автомобиль'
        }
        response = self.client.post('/api/cars/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_car_authenticated(self):
        """Тест на обновление автомобиля для владельца"""
        self.client.credentials(Authorization='Bearer ' + self.token)
        data = {'description': 'Обновленное описание автомобиля'}
        response = self.client.put(f'/api/cars/{self.car.id}/', data, format='json')  # car_id в URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Обновленное описание автомобиля')

    def test_update_car_by_non_owner(self):
        """Тест на попытку обновить автомобиль другим пользователем"""
        # Создаем другого пользователя
        other_user = User.objects.create_user(username='otheruser', password='password123')
        other_token = self.get_jwt_token()
        self.client.credentials(Authorization='Bearer ' + other_token)
        data = {'description': 'Попытка обновить описание'}
        response = self.client.put(f'/api/cars/{self.car.id}/', data, format='json')  # car_id в URL
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_car_authenticated(self):
        """Тест на удаление автомобиля для владельца"""
        self.client.credentials(Authorization='Bearer ' + self.token)
        response = self.client.delete(f'/api/cars/{self.car.id}/')  # car_id в URL
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.filter(id=self.car.id).count(), 0)

    def test_delete_car_by_non_owner(self):
        """Тест на удаление автомобиля другим пользователем"""
        # Создаем другого пользователя
        other_user = User.objects.create_user(username='otheruser', password='password123')
        other_token = self.get_jwt_token()
        self.client.credentials(Authorization='Bearer ' + other_token)
        response = self.client.delete(f'/api/cars/{self.car.id}/')  # car_id в URL
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comments(self):
        """Тест на получение комментариев к автомобилю"""
        response = self.client.get(f'/api/cars/{self.car.id}/comments/')  # car_id в URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Отличный автомобиль!')

    def test_add_comment_authenticated(self):
        """Тест на добавление комментария к автомобилю для аутентифицированного пользователя"""
        self.client.credentials(Authorization='Bearer ' + self.token)
        data = {'content': 'Очень хороший автомобиль!'}
        response = self.client.post(f'/api/cars/{self.car.id}/comments/', data, format='json')  # car_id в URL
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Очень хороший автомобиль!')

    def test_add_comment_unauthenticated(self):
        """Тест на добавление комментария к автомобилю для неаутентифицированного пользователя"""
        data = {'content': 'Очень хороший автомобиль!'}
        response = self.client.post(f'/api/cars/{self.car.id}/comments/', data, format='json')  # car_id в URL
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
