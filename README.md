## Personal Library Management System API:

A simple API that allows users to manage their personal library of books.

## Requirements

To run this application, you will need:

* Docker installed on your machine
* A terminal or command prompt

## Installation

To install this application, follow these steps:

* Clone this repository to your machine: `git clone https://github.com/JHorlamide/library-mgmt-system-api.git`
* Navigate to the project directory: `cd library-mgmt-system-api`

## Running the Application

To start the application use docker compose:

* From the root directory run: `docker-compose up --build -d`
* To test the API endpoints, you can use a tool like [Postman](https://www.postman.com/downloads/) or [curl](https://curl.se/). For example, to create a new resource using `curl`, you can run the following command:

  * ```
    curl -X POST -H "Content-Type: application/json" -d '{ "title": "Growth", "author": "Scale the business", "isben": "9780743273565" }' http://localhost:8000/books/
    ```

## Usage

#### API Endpoints:

The API endpoints of the service are described below:

* `GET /books/`: Get all books belonging to the authenticated user.
* `GET /books/:bookId:` Get book by ID
* `POST /books/`: Create a new book.
* `PUT /books/:bookId:` Update a book with the given ID
* `DELETE /api/:bookId:` Delete a book with the given ID

## Reading the docs

To access the API documentation open `http://127.0.0.1:8000/swagger/` in your broswer.

## Running Test

To ensure the reliability and accuracy of the application, I have implemented a simple suite of tests. While these tests are not exhaustive, but they cover some critical aspects of the API implementation. To run the tests, use the following commands:

* From the root Directory of the project run: `python manage.py test`

I take application testing seriously and am committed to ensuring the highest possible quality of software :)
