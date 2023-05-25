# Backend
Бекенд

Загалом, тут все, що я маю. В мене бекенд до сайту по сервісу кредитування, де користувач може взяти кредит і його погасити

В тому файлі openapi є той код до Rest Api, вставиш цей код на сайті https://editor.swagger.io/ щоб подивитись, що то є таке
Віртуалка в мене Flask

Треба добавити такі штуки:
- до ORM треба добавити таку штуку, як alembic для міграцій у моїй базі даних
- далі треба зробити валідацію даних через пакет marsmellow і захешувати пароль через пакет  FLask-Bscrypt
- для авторизації та автентифікація треба все зробити через пакет Bearer (з JWT-токеном)для кращої реалізації краще використати пакет Flask-JWT
- ну і покрити це все тестами

Для кращого розуміння задач я кидаю ссилки, що конкретно і до чого
- https://github.com/shymanskyivm/Labs_For_Application_Programming/tree/main/Lab%206 
- https://github.com/shymanskyivm/Labs_For_Application_Programming/tree/main/Lab%207 
- https://github.com/shymanskyivm/Labs_For_Application_Programming/tree/main/Lab%208 
- https://github.com/shymanskyivm/Labs_For_Application_Programming/tree/main/Lab%209

Ще даю ссилку на репозиторій мого одногрупника, як приклад, як би воно мало виглядати
https://github.com/StepanSa/AP_Project
