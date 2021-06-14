# Challenge Ripio
Allows send coins between users.
## REQUIREMENTS
- Install python 3.9
- Install pip3
- Install postgres>12
- Install virtualenv
- Install libs run the sentence `pip3 install -r requirements.txt`.
- Create database on postgress called `ripio_challenge`.
- Activate entorno de desarrollo `source venv/bin/activate`
- Run the sentence `python manage.py migrate`.
- Install RabbitMQ.

# Start
- Swagger `http://localhost:8000/api/doc`
- Import postman files from the postam folder located in the project.
- Start RabbitMQ
- Create superuser `python manage.py createsuperuser`.
- Create an account for the superuser in the database with a balance > 0.0
- Create a wallet for the superuser in the database.
- Create a transaction in the database where the sender is the wallet of the superuser and recipient the wallet of a new user.

# Endpoints
- Create an account `/api/v1/auth/register/`
- login `/api/v1/auth/token/`
- Create coins `/api/v1/blockchain/coins/`
- Create an wallet by account `/api/v1/blockchain/wallets/`
- Create a transaction between users `/api/v1/blockchain/wallets/11/transactions`
# Unit test
- Run the sentence `python manage.py test`