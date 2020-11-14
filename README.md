# telegram_quiz
Репозиторий представляет собой бота для повторения материала, который берется из гугл таблиц ([шаблон](https://docs.google.com/spreadsheets/d/1yRJymuVtF-T_b0jpL4y-gkW7gRBAjgKeyUgouuR3XyY/edit?usp=sharing)) и несколько раз в неделю рекомендует студенту ответить на тот или иной вопрос.

## Запуск
Запуск бота рекомендуется через Docker-контейнер:
- Скопировать `credentials.json` из настроек Google Spreadsheet API в корень проекта
- `docker build . -t telegram_quiz`
- `docker run -d telegram_quiz`

## Использование
В Google-таблицу нужно добавить алиасы пользователей в Telegram, и на каждую тему создать свой лист из шаблона. Бот начнет использовать эти данные автоматически, после нового кэширования материала.

## Telegram
Протестировать бота можно по ссылке https://t.me/goodline_quiz_bot