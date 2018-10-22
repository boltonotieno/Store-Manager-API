# Store-Manager-API

[![Maintainability](https://api.codeclimate.com/v1/badges/348eef7a5f2e9c4300b6/maintainability)](https://codeclimate.com/github/BoltC0rt3z/Store-Manager-API/maintainability)
[![Build Status](https://travis-ci.org/BoltC0rt3z/Store-Manager-API.svg?branch=ch-integrate-travis-CI-161312234)](https://travis-ci.org/BoltC0rt3z/Store-Manager-API)
[![Coverage Status](https://coveralls.io/repos/github/BoltC0rt3z/Store-Manager-API/badge.svg?branch=ch-integrate-travis-CI-161312234)](https://coveralls.io/github/BoltC0rt3z/Store-Manager-API?branch=ch-integrate-travis-CI-161312234)


Store Manager is a web application that helps store owners manage sales and product inventory
records.

Features Endpoints:
POST /api/v1/auth/registration      Creates a user account

POST /api/v1/auth/login     Login a user

GET /api/v1/auth/users      Gets all users

GET /api/v1/auth/users/user_id      Gets a single user by user id

POST /api/v1/products       Add a product

POST /api/v1/sales      Add a sales record

GET /api/v1/products    Retrieve all products

GET /api/v1/sales       Retrieve all sales records

GET /api/v1/products/productId  Retrieve a single product by id

GET /api/v1/sales/sale_id        Retrieve a single sales record by id
