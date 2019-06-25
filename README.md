# epg

# epg

## Развертка рабочего проекта
Для разработки создаем виртуальное окружение с python3:

`virtualenv -p python3 epg_ve`

После этого активируем его соответсвенно командой:

`source /path/to/epg_ve/bin/activate`

Переходим в папку с проектом:

`cd /path/to/epg_ve`

и запускаем установку зависимостей:

`pip install -r requirements/requirements.txt`

После установки зависмиостей идем в каталог проекта **configs/settings** и создаем файл **local.py**

Пример содержания есть в файле **local.py.example**

Для нормальной работы необходим redis-server, т.к. сессии пользователей и оперативны кэш хранятся в нем.
Redis так же используется в качестве брокера для Celery.
Коенчно локально можно и поменять настройки.

После всех манипуляций необходимо применить миграции:

`python manage.py migrate`

## local.py
Этот файл занесен в **.gitignore** и предназначен для указания специфических локальных настроек.

Для разработки файл local.py должен начинаться с импорта:

`from .dev import *`

Для развертки в production-окружении соответсвенно:

`from .production import *`

Параметр SECRET\_KEY вынесен из бызовых настроек и его также нужно указать в **local.py** (на то он и SECRET)

Так же там необходимо указать параметры соединения с БД - **DATABASES**

Так же в production-окружении в этот фал желательно писать доступы к каким-то внешним сервисам, которые всем подряд знать необязательно.

Ну и в принципе в нем можно переопределить любые базовые настройки


Создание базы и пользователя в postgres:

```bash
sudo -u postgres psql
```

```SQL
CREATE USER epgdb WITH PASSWORD 'epg_pass';

CREATE DATABASE epgdb
  WITH OWNER = epgdb
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'ru_RU.UTF-8'
       LC_CTYPE = 'ru_RU.UTF-8'
       CONNECTION LIMIT = -1;

GRANT CONNECT, TEMPORARY ON DATABASE epgdb TO public;
GRANT ALL ON DATABASE epgdb TO postgres;
GRANT ALL ON DATABASE epgdb TO epgdb;
```
