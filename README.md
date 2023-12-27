Все команды вводятся в директории проекта:<br />
		mkdir flask_auth_app <br />
 		cd flask_auth_app<br />
<br />
1. Установка необходимых пакетов:<br />
		pip install python3<br />
		python3 -m venv auth<br />
		sudo apt install mysql-server mysql-client<br />
2. Добавление базы данных:<br />
   		mysql<br />
   		create user 'admin'@'localhost' identified by 'admin';<br />
   		grant all privileges on * . * to 'admin'@'localhost';<br />
   		create database dotacamp;<br />
   		use dotacamp;<br />
   		create table users(id INT, login TEXT, password TEXT, id_post INT, is_admin BOOLEAN);<br />
   		create table posts(id INT, id_author INT, text TEXT, img_path TEXT);<br />
   		create table scores(id INT, id_user INT, id_post INT, score INT);<br />
   		exit;<br />
4. Активация виртуальной среды и её настройка:<br />
		source auth/bin/activate<br />
		pip install flask flask-sqlalchemy flask-login<br />
		mkdir ourproject<br />
		После необходимо перенести все файлы проекта в новосозданную папку ourproject.<br />
		export FLASK_APP=project<br />
		export FLASK_DEBUG=1					// Необязательно, необходимо для отслеживания ошибок<br />
		flask run						// Может потребоваться ключ --host="0.0.0.0"<br />
<br />
Для перехода на страницы приложения: localhost:5000<br />
