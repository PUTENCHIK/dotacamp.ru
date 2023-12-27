Все команды вводятся в директории проекта:
		mkdir flask_auth_app
 		cd flask_auth_app

1. Установка необходимых пакетов:
		pip install python3
		python3 -m venv auth
2. Активация виртуальной среды и её настройка:
		source auth/bin/activate
		pip install flask flask-sqlalchemy flask-login
		mkdir ourproject
		После необходимо перенести все файлы проекта в новосозданную папку ourproject.
		export FLASK_APP=project
		export FLASK_DEBUG=1					// Необязательно, необходимо для отслеживания ошибок
		flask run											// Может потребоваться ключ --host="0.0.0.0"

Для перехода на страницы приложения: localhost:5000
