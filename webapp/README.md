# Ghostwriter

講義内容代筆アプリケーション名．

## Environment

* Python 3.6~
* Django 1.11.6
* OpenCV 3.3.0
* Docker for Mac

## Usage

install dependencies

```bash
$ git clone https://github.com/jphacks/KB_1708.git
$ cd webapp
$ pip install -r requirements.txt
$ brew tap homebrew/science
$ brew install opencv3 --with-python3
$ docker pull rabbitmq:latest
```

run migrate

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

run rabbitmq

```bash
$ docker run --rm -it --name broker -p 5672:5672 rabbitmq:latest
```

run celery tasks

```bash
$ pwd
/path/to/webapp
$ celery -A webapp worker
```

You want to capture the slides, you should run following task.

```bash
$ python manage.py capture
```

Finally, 

1. Access `127.0.0.1:8000`
2. Select `Capture Now`
3. `OK`
4. Select `HOME`
5. Select capture image which you want them to add lecture.
6. Select lecture (Left column)
7. Select `保存`
8. Go to `Lecture` and select lecture.
9. you will get OCR text and questions (when press `問題生成`)

