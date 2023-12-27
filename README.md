Все команды вводятся в директории проекта:
		mkdir flask_auth_app
 		cd flask_auth_app

1. Установка необходимых пакетов:
		pip install python3
		python3 -m venv auth
		sudo apt install mysql-server mysql-client
2. Добавление базы данных:
   		mysql
   		create user 'admin'@'localhost' identified by 'admin';
   		grant all privileges on * . * to 'admin'@'localhost';
   		create database dotacamp;
   		use dotacamp;
   		create table users(id INT, login TEXT, password TEXT, id_post INT, is_admin BOOLEAN);
   		create table posts(id INT, id_author INT, text TEXT, img_path TEXT);
   		create table scores(id INT, id_user INT, id_post INT, score INT);
   		exit;
4. Активация виртуальной среды и её настройка:
		source auth/bin/activate
		pip install flask flask-sqlalchemy flask-login
		mkdir ourproject
		После необходимо перенести все файлы проекта в новосозданную папку ourproject.
		export FLASK_APP=project
		export FLASK_DEBUG=1					// Необязательно, необходимо для отслеживания ошибок
		flask run											// Может потребоваться ключ --host="0.0.0.0"

Для перехода на страницы приложения: localhost:5000
