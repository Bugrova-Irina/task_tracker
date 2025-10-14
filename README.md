# Трекер задач сотрудников на DjangoRestFramework
```python manage.py runserver``` - запуск веб-приложения. Ctrl+C - остановка сервера.

```python manage.py createadmin``` - создание суперпользователя

```python manage.py test``` - запуск тестов

## Описание:

Серверное приложение для работы с базой данных, представляющее собой трекер
задач сотрудников. В приложении есть обычные пользователи, которые могут создавать
задачи, видеть список своих задач, просматривать подробную информацию о задаче,
редактировать и удалять свои задачи. Пользователь может просматривать, редактировать и
удалять свой профиль. Менеджер может видеть список всех пользователей и задач, просматривать
подробную информацию о задаче и любом пользователе, но не может их редактировать, кроме
своих задач и своего профиля. Может назначать исполнителя задаче. Менеджер должен состоять 
в группе managers.


## Требования к окружению:

Установите:
 - python 3.13.0
 - Poetry
 - Django
 - Pillow
 - python-dotenv
 - psycopg2 или psycopg2-binary
 - djangorestframework
 - djangorestframework-simplejwt
 - flake8
 - black
 - isort
 - ipython


В качестве базы данных используется PostgreSQL

## Установка:

1. Клонируйте репозиторий:
```
https://github.com/Bugrova-Irina/homework_30.1_drf/
```
2. Установите зависимости:
```
poetry shell
```
```
poetry add django
```
```
poetry add Pillow
```
```
poetry add psycopg2
```
```
poetry add python-dotenv
```
```
poetry add djangorestframework
```
```
poetry add djangorestframework-simplejwt
```
```
poetry add flake8
```
```
poetry add black
```
```
poetry add isort
```
```
poetry add ipython
```

3. Запустите Redis

## Использование:

После запуска сервера перейдите по ссылке http://127.0.0.1:8000/tasks/.

### Запуск проекта с использованием Docker Compose:
В корне проекта должны быть файлы:
- Dockerfile
- docker-compose.yml
- .env (создайте на основе .env.sample со своими значениями)

#### Команды для запуска:
Выполните сборку образов:
```
docker-compose build
```

Запуск контейнеров в фоновом режиме:
```
docker-compose up -d
```

Убедитесь, что все контейнеры запущены:
```
docker-compose ps
```

Примените миграции базы данных:
```
docker-compose exec web python manage.py migrate
```

Создайте учетную запись администратора
```
docker-compose exec web python manage.py createsuperadmin
```

Проверка работы приложения:
Перейдите по адресу: http://localhost:8002/tasks/

#### Проверка работоспособности сервисов
1. Веб-сервис (Django). Откройте в браузере http://localhost:8002/ или выполните команду:
```
curl -X GET http://localhost:8002/tasks/
```
2. База данных (PostgreSQL):
```
docker-compose exec db psql -U your_database_user -d your_database_name -c "\dt"
```
Результат: должен отобразить список таблиц в базе данных.

3. Redis:
```
docker-compose exec redis redis-cli ping
```
Результат: должен вернуть PONG.

4. Celery Worker:
```
docker-compose logs celery
```
Результат: в логах должны быть сообщения об успешном запуске worker.

5. Celery Beat:
```
docker-compose logs beat
```
Результат: в логах должны быть сообщения о запуске планировщика.

6. Административная панель Django:
Откройте в браузере http://localhost:8002/admin/

7. Остановка контейнеров:
```
docker-compose down
```
8. Перезапуск с пересборкой образов:
```
docker-compose up -d --build
```
Просмотр логов конкретного сервиса (web, db, redis, celery, beat):
```
docker-compose logs [service_name]
```

## Настройка удаленного сервера и деплоя
1. Установите Python 3.13.
2. Установите Django версии 3.2.
3. Установите Gunicorn и Nginx для обработки запросов.

#### Подключение к серверу:
```
ssh username@server_ip
```

#### Обновление системы:
```
sudo apt update && sudo apt upgrade -y
```

#### Установка базовых пакетов:
```
sudo apt install -y curl wget git htop nano ufw
```

#### Настройка брандмауэра:
```
sudo ufw allow ssh
```
```
sudo ufw allow 80
```
```
sudo ufw allow 443
```
```
sudo ufw enable
```

### Настройка сервера
1. Настройте SSH-доступ с использованием SSH-ключей для повышения безопасности.
2. Закройте все ненужные порты, оставив открытыми только те, которые необходимы (например, 80 для HTTP и 443 для HTTPS).
3. Установите и настройте Supervisor для автоматического перезапуска приложения при изменениях.

### Создание пользователя для деплоя
Создание пользователя
```
sudo adduser deployer
```
```
sudo usermod -aG sudo deployer
```

Настройка SSH-доступа
```
sudo mkdir /home/deployer/.ssh
```
```
sudo cp ~/.ssh/authorized_keys /home/deployer/.ssh/
```
```
sudo chown -R deployer:deployer /home/deployer/.ssh
```
```
sudo chmod 700 /home/deployer/.ssh
```
```
sudo chmod 600 /home/deployer/.ssh/authorized_keys
```

### Настройка Docker и Docker Compose
#### Установка Docker
```
curl -fsSL https://get.docker.com -o get-docker.sh
```
```
sudo sh get-docker.sh
```
#### Добавление пользователя в группу docker
```
sudo usermod -aG docker $USER
```
```
sudo usermod -aG docker deployer
```
#### Перезагрузка сессии
```
newgrp docker
```
#### Проверка установки
```
docker --version
```
#### Установка Docker Compose
#### Скачивание последней версии
```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
#### Назначение прав
```
sudo chmod +x /usr/local/bin/docker-compose
```
#### Проверка установки
```
docker-compose --version
```
### Деплой
1. Склонируйте репозиторий на сервер.
2. Выполните миграции базы данных с помощью команды python manage.py migrate.
3. Запустите сервер с помощью Gunicorn: gunicorn myproject.wsgi:application.
4. Настройте Nginx для проксирования запросов к Gunicorn.

### Выполните на сервере команды:
На сервере настроен systemd для автоматического управления.
#### Создание systemd сервиса
```
sudo nano /etc/systemd/system/myapp.service
```

Приложение будет автоматически запускаться и перезапускаться при изменениях или сбоях
```
sudo systemctl daemon-reload
```
```
sudo systemctl restart myapp.service
```
```
sudo systemctl status myapp.service
```
Удаленный сервер может автоматически перезагружать приложение при внесении изменений.
Workflow запускается при каждом push в репозиторий. Проект автоматически деплоится 
на удаленный сервер. Все чувствительные данные вынесены в переменные окружения и 
подключены к workflow через Secrets GitHub. В secrets and variables задайте секреты

DEPLOY_DIR
DOCKER_HUB_ACCESS_TOKEN
DOCKER_HUB_USERNAME
SECRET_KEY
SERVER_IP
SSH_KEY
SSH_USER

Проверьте работу приложения по адресу http://your_server_name/tasks/

#### Команды для мониторинга работы приложения на сервере
#### Статус приложения
```
sudo systemctl status myapp.service
```
#### Логи приложения
```
sudo journalctl -u myapp.service -f
```
#### Логи Docker контейнера
```
docker logs myapp
```
#### Использование ресурсов
```
docker stats myapp
```
#### Проверка сети
```
sudo netstat -tulpn | grep :80
```
#### Проверка доступности
```
curl -I http://localhost/
```

## Тестирование:

Добавлено тестирование корректности работы CRUD уроков и функционала работы подписки
на обновления курса. Добавлен отчет о покрытии тестами в папке htmlcov/index.html.

## Документация:

Для проекта подключен и настроен вывод документации с помощью drf-yasg.

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)