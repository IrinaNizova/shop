sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev

CREATE USER user WITH PASSWORD 'myPassword';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "user";
systemctl restart postgresql