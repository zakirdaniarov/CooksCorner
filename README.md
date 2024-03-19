# CooksCorner
CooksCorner is an innovative offering designed to provide a convenient and inspiring experience in the world of cooking. 
Offering a variety of categories including an extensive list of recipes, CooksCorner creates a user-friendly platform for culinary enthusiasts. 
Immerse yourself in culinary delights with breathtaking photography, explore detailed recipe descriptions, and manage your culinary experience by saving, liking, and even creating your own dishes.
CooksCorner is your gateway to hassle-free and inspiring culinary adventures.

### Technologies
---
- Python
- Django Rest Framework
- Swagger UI
- Nginx
- Docker

### Install
---
#### Without docker
1. Clone repository to your local machine:
```
git clone ssh/https-key
```
2. Create virtual environment and activate virtual environment:
- On `Windows`:
```
python -m env venv
```
```
venv\Scripts\activate.bat
```
- On `Linux/MacOs`
```
python3 -m env venv
```
```
source venv/bin/activate
```
3. Add `.env` file to the root and fill with your data next variables:
```
DB_HOST=db
DB_USER=postgres
DB_PASSWORD=postgres_password
DB_NAME=postgres
DB_PORT=5432
POSTGRES_HOST_AUTH_METHOD=trust
DEBUG=True
EMAIL_HOST_USER = 
EMAIL_HOST_PASSWORD = 
```
4. Install all dependecies:
```
pip install -r requirements.txt
```
5. Run the project on your local host:
```
python/python3 manage.py runserver
```
### Authors
---
[Mamatair uulu Zakirbek, 2024](https://github.com/zakirdaniarov)
