# trade_core_api


## Getting started

### Prerequisites

In order to install and run this project locally, you would need to have the following installed on you local machine.

- **Python 3+**
- **Django 4+**
- **Postgresql**

### Installation
* Clone this repository

* Navigate to the project directory `cd trade_core/`

* Create a virtual environment

* Install dependencies `pip3 install -r requirements.txt`
* Edit `trade_core/settings.py` database credentials to your database instance

* Create a Postgresql database 

* Run the command `python3 manage.py makemigrations` 

* Run the command `python3 manage.py migrate` to create and sync the postgresql database (you must have the database previously created with name 'hub_db').

* Run the command `python3 manage.py runserver`

* Run development server

* To run tests `python manage.py test`

* To run test coverage `coverage report -m`


## Testing API endpoints
<table>
<tr><th>Test</th>
<th>API-endpoint</th>
<th>HTTP-Verbs</th>
</tr>
<tr>
<td>Register a user</td>
<td>/users/register/</td>
<td>POST</td>
</tr>
<tr>
<td>Login a user</td>
<td>/users/login/</td>
<td>POST</td>
</tr>
<tr>
<td>View a single user</td>
<td>/users/details/</td>
<td>GET</td>
</tr>
<tr>
<td>Create a post </td>
<td>/api/posts/</td>
<td>POST</td>
</tr>
<tr>
<td>View all posts</td>
<td>/api/posts/</td>
<td>GET</td>
</tr>
<tr>
<td>View a single post</td>
<td>/api/posts/<:id></td>
<td>GET</td>
</tr>
<tr>
<td>Update a post</td>
<td>/api/posts/<:id></td>
<td>PUT</td>
</tr>
<tr>
<td>Delete a single post</td>
<td>/api/posts/<:id></td>
<td>DELETE</td>
</tr>
<tr>
<td>Like a single post</td>
<td>/api/posts/like/<:id></td>
<td>POST</td>
</tr>
<tr>
<td>Unlike a single post</td>
<td>/api/posts/dislike/<:id></td>
<td>POST</td>
</tr>
<tr>

</table>


### Authors
- Arnold Osoro - [mmosoroohh](https://github.com/mmosoroohh)
