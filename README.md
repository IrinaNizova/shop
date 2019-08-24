Для работы проекта необходимо установить базу postgres
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev

Создаём пользователя
CREATE USER user WITH PASSWORD 'myPassword';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "user";
systemctl restart postgresql

Прописываем данные для подключения к базе в файл shop/settings.py в блок DATABASES

apt-get install python3-pip
Устанавливаем нужные пакеты: pip3 install -r requirements.txt

выполняем миграции
python3 manage.py makemigrations shop
python3 manage.py migrate

Для запуска на сервере:
sudo apt-get install nginx
sudo apt-get gunicorn3
gunicorn3 -b 0.0.0.0:8080 shop.wsgi:application

Запуск тестов
python3 manage.py test