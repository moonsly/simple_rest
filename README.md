simple_rest
===========

Simple REST on django with social auth, django rest framework + python-social-auth

Запросы REST API:

GET /api/user – return user info about current user in JSON format `{“first_name”:”Sandra”,”last_name”:”Bullock”,”gender”:”female”,”age”:48}`

PATCH /api/user – updates info about current user JSON `{“first_name”:”Sandra”,”last_name”:”Bullock”,”gender”:”female”,”age”:49}`
On success update returns 202 HTTP code.

GET /api/users?age={integer} – returns IDs of all users in JSON format, 
`[123,521,415,875]`
if optional age parameter is specified - only users of this age.

GET /api/users/{user-id} – returns info about user with ID=user-id in JSON format
`{“first_name”:”Sandra”,”last_name”:”Bullock”,”gender”:”female”,”age”:49}.`

Authentication of new users is implemented via OAuth 2.0 protocol, Facebook and VK.com are supported. During the first user's social authorisation in pipeline some additional info is extracted from social APIs with users' social ID.

