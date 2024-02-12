# Project 1
## Welcome to my book Review Website.
#### ENGO 651

This website offers a comprehensive platform for book enthusiasts to explore and share their insights on a vast collection of books. Below is an overview of the website's capabilities and the structure of the project:

### Features
* User Registration: New visitors can easily sign up to access the website's features.
* User Authentication: Secure login and logout functionality for a personalized experience.
* Book Discovery: Users can search for books by ISBN, title, or author, facilitating easy discovery of their next read.
* Book Details: For each book, users can view essential information such as ISBN, title, author, year of publication, and user reviews.
* Review Submission: Readers can contribute to the community by rating books and leaving textual comments.

### Project Structure

* books.csv: Contains comprehensive data on books covered by the website.
* import.py: A script designed to read information from books.csv and populate the database with book data.
* application.py: The core of the web application, defining all the routes and functionalities.

### Templates

* index.html: The homepage that doubles as the login page. New users are directed here to register.
* register.html: Dedicated to new user registration for those who do not yet have an account.
* search.html: Enables users to search for books using partial or full ISBNs, titles, or author names. Displays matching results.
* book.html: Displays detailed information about a selected book from the search results, including user reviews. Here, users can also   submit their ratings and comments.


