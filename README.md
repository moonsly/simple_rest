simple_rest
===========

Simple REST on django with social auth, django rest framework + python-social-auth

Запросы REST API:

GET /api/user – возвращает имя, фамилию, пол и возраст текущего пользователя в формате JSON {“first_name”:”Sandra”,”last_name”:”Bullock”,”gender”:”female”,”age”:48}

PATCH /api/user – обновляет информацию о текущем пользователе. Тело запроса в формате JSON {“first_name”:”Sandra”,”last_name”:”Bullock”,”gender”:”female”,”age”:49}.  В случае успешного обновления возвращается 202 код статуса.

GET /api/users?age={integer} – возвращает список идентификаторов пользователей в формате JSON [123,521,415,875]. Параметр age (опциональный) позволяет выбрать пользователей имеющих определенный возраст.

GET /api/users/{user-id} – возвращает информацию о пользователе заданном идентификатором user-id в формате JSON {“first_name”:”Sandra”,”last_name”:”Bullock”,”gender”:”female”,”age”:49}.

Аутентификация в приложении через соц.сети ВКонтакте, Facebook, авторизация API по протоколу OAuth 2.0. При первой аутентификации из соц. сети подгружаются имя, фамилия, пол и возраст. Данные значения используются значениями по умолчанию для полей локальной БД.

