# Bibliotek
Book management tool, developped in the scope of the Applications in Object-oriented Programming and Databases course.

Classes of **Bibliotek** are described below. Some of them are **resources** for the rest api, some are **models** used to update the database and also some are  webscraping class components required by **Scrapy**.

# Installation
## Windows
    pip3 install -r requirements.txt
## OSX / Linux
    sudo pip3 install -r requirements.txt

# Run the flask app
To start the Flask API

    python3 app.py

Then the server will be started in the terminal. 

To stop the process : `CTRL+C`

# (Optional) run only the scraping
First you need to be in the `bibliotek/bibliotek` folder.

    scrapy crawl books -a title="YourTitleHere" -a authors="YourAuthorsHere" -a isbn="YourIsbnHere"

# Database

You must set the **`DB_USER`** and **`DB_PASSWORD`** with credentials provided in the executive summary.

# FLASK API API
## Documentation is available <a href="https://documenter.getpostman.com/collection/view/2471406-227dcc87-8dbe-e51d-264a-c6b929bc3593">here</a>
### Resources
    author
        1. Author
        2. AuthorName
        3. AuthorList
    book
        1. Book
        2. BookTitle
        3. BookList
        4. BookCategories
        5. BookAuthors
        6. BookSearch
    category
        1. Category
        2. CategoryName
        3. CategoryList
    portfolio_book
        1. PortfolioBook
        2. PortfolioBookList
        3. PortfolioBookEdit
    portfolio
        1. Portfolio
        2. PortfolioList
        3. PortfolioUser
    user
        1. UserRegister
        2. UserList
        3. User
        4. UserEmail
### Models
    author
        1. AuthorModel
    book
        1. BookModel
    category
        1. CategoryModel
    portfolio_book
        1. PortfolioBookModel
    portfolio
        1. PortfolioModel
    user
        1. UserModel

# Scrapy
## Models
That are required by scrapy for storing and processing data gathered on websites.
They are Stored through the model and Processed through a pipeline.

    Items
        - Book
    Pipelines
        - APICallerPipeline

## Controllers
For scrapy, controllers may be interpreted by the spiders. Because all of the manipulation is done by the spider.
A spider is the engine that will search web pages and gather data. Data which, will be then stored into the model and processed by the pipeline.

    Spiders
        - BooksSpider

# Book Info
Class which purpose is to gather additionnal book information on google book API.

    book_info
        - BookInfo
