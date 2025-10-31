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
в группе managers. Суперпользователь может редактировать любые задачи и видеть список
всех задач.

По ссылке http://127.0.0.1:8000/users/ доступен список сотрудников и их задач, отсортированный
по количеству активных задач.

По ссылке http://127.0.0.1:8000/tasks/no-executor/ доступен список активных задач, которые 
не взяты в работу (не заполнено поле executor), но от которых зависят другие задачи, взятые
в работу, как родительские, так и дочерние.

По ссылке http://127.0.0.1:8000/tasks/important-with-candidates/ доступен список пользователей,
которые могут взять в работу задачи, от которых зависят другие задачи, уже взятые в работу.
Информация выводится в формате "название задачи" - "срок исполнения" - "список пользователей,
которые могут взять задачу в работу":
```
{
            "task": {
                "id": 3,
                "title": "write some code",
                "time": "2025-10-15T10:10:00Z"
            },
            "deadline": "2025-10-15T10:10:00Z",
            "candidates": [
                {
                    "id": 7,
                    "full_name": "Juliy Cezar",
                    "active_tasks_count": 0
                },
                {
                    "id": 4,
                    "full_name": "Admin Adminov",
                    "active_tasks_count": 0
                }
            ]
        }
```

Добавлены тесты для tasks и users.

Настроена API-документация.

Настроена защита пользователей от несанкционированного доступа к данным на разных доменах
с помощью CORS.

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
 - coverage
 - drf-yasg
 - django-cors-headers
 - gunicorn


В качестве базы данных используется PostgreSQL

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/Bugrova-Irina/task_tracker/
cd task_tracker
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
```
poetry add coverage
```
```
poetry add drf-yasg
```
```
poetry add django-cors-headers
```
```
poetry add gunicorn
```

3. Создайте файл `.env` на основе `.env.sample`
4. Заполните переменные окружения в `.env` файле.

## Использование:

После запуска сервера перейдите по ссылке http://127.0.0.1:8000/tasks/.

### Запуск проекта с использованием Docker Compose (для разработки):

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
docker-compose exec backend python manage.py migrate
```

Создайте учетную запись администратора
```
docker-compose exec web python manage.py createadmin
```

Проверка работы приложения:
Перейдите по адресу: http://localhost:8080/tasks/

#### Проверка работоспособности сервисов
1. Веб-сервис (Django):
```
curl -X GET http://localhost:8002/tasks/
```
2. База данных (PostgreSQL):
```
docker-compose exec db psql -U your_database_user -d your_database_name -c "\dt"
```
Результат: должен отобразить список таблиц в базе данных.

3. Административная панель Django:
Откройте в браузере http://localhost:8080/admin/

4. Остановка контейнеров:
```
docker-compose down
```
5. Перезапуск с пересборкой образов:
```
docker-compose up -d --build
```
Просмотр логов конкретного сервиса (web, db, redis, celery, beat):
```
docker-compose logs [service_name]
```

## Автоматический деплой на продакшн-сервер
Проект настроен для автоматического деплоя на сервер при каждом пуше в основную ветку
репозитория.

## Настройка удаленного сервера для деплоя

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

### Установка Docker и Docker Compose:
```
curl -fsSL https://get.docker.com -o get-docker.sh
```
```
sudo sh get-docker.sh
```
```
sudo usermod -aG docker $USER
```
```
newgrp docker
```
```
docker --version
```
```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
```
docker-compose --version
```
#### Подготовка директории на сервере:
```
sudo mkdir -p /opt/task_tracker
sudo chown $USER:$USER /opt/task_tracker
cd /opt/task_tracker
```
### Настройка CI/CD с GitHub Actions

#### Необходимые секреты в GitHub:

В настройках репозитория GitHub добавьте следующие секреты:

- `DEPLOY_DIR` - `/opt/task_tracker`
- `DOCKER_HUB_ACCESS_TOKEN` - токен доступа Docker Hub
- `DOCKER_HUB_USERNAME` - ваш логин Docker Hub
- `SECRET_KEY` - секретный ключ Django
- `SERVER_IP` - IP адрес сервера
- `SSH_KEY` - приватный SSH ключ для доступа к серверу
- `SSH_USER` - пользователь сервера

#### Процесс деплоя:

1. При пуше в основную ветку автоматически запускается GitHub Actions workflow
2. Выполняются тесты и линтинг кода
3. Собирается Docker образ и пушится в Docker Hub
4. Образ автоматически деплоится на продакшен-сервер

### Ручной деплой на сервер

#### На сервере создайте необходимые файлы:

1. `docker-compose.prod.yml` - конфигурация для продакшена
2. `.env` - переменные окружения
3. `nginx.conf` - конфигурация nginx
4. `deploy.sh` - скрипт деплоя

#### Пример deploy.sh:
```
bash
#!/bin/bash
cd /opt/task_tracker
docker-compose -f docker-compose.prod.yml down
docker pull your-dockerhub-username/task_tracker:latest
docker-compose -f docker-compose.prod.yml up -d
docker image prune -f
echo "Deployment completed successfully!"
```
Сделайте скрипт исполняемым:
```
chmod +x deploy.sh
```
Запуск деплоя:
```
./deploy.sh
```

## Проверка работы приложения на сервере
После деплоя проверьте:
1. Статус контейнеров:
```
docker-compose -f docker-compose.prod.yml ps
```
2. Логи приложения:
```
docker-compose -f docker-compose.prod.yml logs backend
```
3. Доступность API:
```
curl http://localhost/tasks/
```
4. Документация:
- API: http://your-server-ip/tasks/
- Админка: http://your-server-ip/admin/
- Swagger: http://your-server-ip/swagger/
- ReDoc: http://your-server-ip/redoc/

## Тестирование:

Добавлено тестирование корректности работы CRUD задач и пользователей. 
Добавлен отчет о покрытии тестами в папке htmlcov/index.html.

1. Запуск тестов с покрытием
```
coverage run --source='.' manage.py test
```
2. Генерация HTML отчета
```
coverage html
```
## Документация:

Для проекта подключен и настроен вывод документации с помощью drf-yasg.
```
http://127.0.0.1:8000/redoc/
```
```
http://127.0.0.1:8000/swagger/
```

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)