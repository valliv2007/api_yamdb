# Project API YAMDB
### Description:
In the Yamdb project, you can leave a review on works ("Books", "Movies", "Music", etc.). Reviews consist of a text note and a rating from 1 to 10. The rating is calculated based on the ratings given by users. Works can be filtered by category or genre.
### How to run the project:
Clone the repository and go to it in the command line::
```sh
git clone https://github.com/valliv2007/api_yamdb.git
```
```sh
cd api_yamdb
```
Create and activate a virtual environment:
```sh
python -m venv venv
```
```sh
source venv/bin/activate or source venv/Scripts/activate
```
Install dependencies from the requirements.txt file:
```sh
pip install -r requirements.txt
```
Run migrations:
```sh
python manage.py migrate
```
Start the project:
```sh
python manage.py runserver
```
## API Request documentation
See yatube_api/static/redoc.yaml or after running it on localhost at http://127.0.0.1:8000/redoc/

### Developed this project
- Snezhko Ilya *(Teamlead)* / GitHub: https://github.com/valliv2007
- Avrov Alexander / GitHub: https://github.com/AlexanderAvrov
- Mishankin Alexey / GitHub: https://github.com/amishankin
