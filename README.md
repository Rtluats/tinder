# tinder
- Перед запуском проекта надо установить библиотеки приведённые ниже через команду: pip install <название библиотеки>
- Запуск сервера производится командой: python manage.py runserver
- Для запуска тестов надо: 
  1. прописать команду в unix: export DJANGO_SETTINGS_MODULE="Tinder.settings"
  2. потом прописать команду для запуска: pytest user_app/tests.p

В проекте используются библеотеки django, djoser, geoip2, pillow (только для фото в базе данных), pytest, rest-framework, psycopg2-binary 

Автор программы Косырев А.С.
