��� ������ ������� ���������� ���������� ���� postgres
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev

������ ������������
CREATE USER user WITH PASSWORD 'myPassword';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "user";
systemctl restart postgresql

����������� ������ ��� ����������� � ���� � ���� shop/settings.py � ���� DATABASES

apt-get install python3-pip
������������� ������ ������: pip3 install -r requirements.txt

��������� ��������
python3 manage.py makemigrations shop
python3 manage.py migrate

��� ������� �� �������:
sudo apt-get install nginx
sudo apt-get gunicorn3
gunicorn3 -b 0.0.0.0:8080 shop.wsgi:application

������ ������
python3 manage.py test