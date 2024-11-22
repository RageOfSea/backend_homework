**Если зачем то хочется запустить это:**

git clone https://github.com/RageOfSea/backend_homework

cd backend_homework

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver



**Если поменяли модели:**


python manage.py makemigrations

python manage.py migrate
