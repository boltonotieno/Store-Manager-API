# Store-Manager-API

[![Maintainability](https://api.codeclimate.com/v1/badges/348eef7a5f2e9c4300b6/maintainability)](https://codeclimate.com/github/BoltC0rt3z/Store-Manager-API/maintainability)
[![Build Status](https://travis-ci.org/BoltC0rt3z/Store-Manager-API.svg?branch=develop)](https://travis-ci.org/BoltC0rt3z/Store-Manager-API)
[![Coverage Status](https://coveralls.io/repos/github/BoltC0rt3z/Store-Manager-API/badge.svg?branch=ch-jwt-authentication-161483424)](https://coveralls.io/github/BoltC0rt3z/Store-Manager-API?branch=ch-jwt-authentication-161483424)


[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/2d0065cf05d793676667)

Store Manager is a web application that helps store owners manage sales and product inventory
records.

### V1 Features Endpoints:
| Method | Route | Endpoint Functionality |
| :---         |     :---       |          :--- |
| POST   | /api/v1/auth/register     | Creates a user account    |
| POST     | /api/v1/auth/login        | Login a user      |
| GET     | /api/v1/users        | Gets all users     |
| GET     | /api/v1/users/user_id      |Gets a single user by id      |
| POST     | /api/v1/product        | Add a product      |
| POST     | /api/v1/sale        | Add a sales record      |
| GET     | /api/v1/product       | Retrieve all products     |
| GET     | /api/v1/product/product_id       | Retrieve a single product by id     |
| GET     | /api/v1/sale       | Retrieve all sales records    |
| GET     | /api/v1/sale/sale_id      | Retrieve a single sales record by id     |

### V2 Features Endpoints:
| Method | Route | Endpoint Functionality |
| :---         |     :---       |          :--- |
| POST   | /api/v2/auth/signup     | Creates a user account    |
| POST     | /api/v2/auth/login        | Login a user      |
| GET     | /api/v2/users        | Gets all users     |
| GET     | /api/v2/users/user_id      |Gets a single user by id      |
| POST     | /api/v2/products        | Add a product      |
| POST     | /api/v2/sales        | Add a sales record      |
| POST     | /api/v2/category       | Add category     |
| GET     | /api/v2/products       | Retrieve all products     |
| GET     | /api/v22/products/product_id       | Retrieve a single product by id     |
| PUT     | /api/v2/products/product_id       | Modify single product    |
| DELETE     | /api/v2/products/product_id       | DELETE single product    |
| GET     | /api/v2/sales       | Retrieve all sales records    |
| GET     | /api/v2/sales/sale_id      | Retrieve a single sales record by id     |
| GET     | /api/v2/category/category_id       | Retrieve single category    |
| GET     | /api/v2/category/category_id       | Retrieve single category    |
| PUT     | /api/v2/category/category_id       | Modify single category   |
| DELETE     | /api/v2/category/category_id       | DELETE single category    |


### Installation Procedure
clone the repo

``` 
git clone https://github.com/BoltC0rt3z/Store-Manager-API

```

create and activate the virtual environment

```
virtualenv <environment name>

```
```
$source <env name>/bin/activate (in bash)

```
install project dependencies:

```
$pip install -r requirements.txt

```
### Running
Running the application
```
python run.py

```
### Testing
Using pytest . The tests are in app/api/test/v1
```
pytest -v
