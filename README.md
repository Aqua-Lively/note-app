# note-app
## FastAPI PostgreSQL 
### О приложении
Авторизация с аутентификацией была реализована с помощью библиотеки FastAPI Users. Реализация этой библиотеки была через SQLAlchemy, CookieTransport, JWTStrategy. 
При создании заметки, её текст проверяет функция check_text. check_text отправляет запрос Яндекс.Сплетеру, в запросе текст заметки, потом функция исправляет ошибки и возвращает финальный текст.  

Подключение к PosgreSQL и использование ассинхронное. И все routes тоже асинхронные. 



### Как запустить
1. Клонируем репозиторий
2. Скачиваем библиотеки
3. Запускаем приложение FastAPI
```
uvicorn main:app --reload
```
4. Запускаем docker-compose
```
docker compose up
```

### Как улучшить
1. Вынести файл database из папки auth 
2. Релизовать нормальную файловую структуру
3. Раскидать по файлам/папкам содержимое файла main.py
4. Воспользоваться средством автоматизированного форматирования исходного кода (yapf или black)
