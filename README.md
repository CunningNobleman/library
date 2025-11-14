# A simple library catalogue management system.
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![FASTAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
\
\
This project was done within a Python course. \
This is a library catalogue management system that supports 
+ User authentication and authorization
+ Storing user reviews
+ Book loans' information.
## Description
There are four tables in this database: `users`, `reviews`, `book loans` and `books`. \
Table users supports several CRUD operations:

1. Posting a new user
2. Getting a token for authorization
3. Updating user entry
4. Deleting an entry.

Similar CRUD - operations supported for other endpoints.

In the *books/book-rankings/rankings* endpoint there is a list of books ranked by their average review score (review is a number between 1 and 5).

## Testing
Testing was performed using `pylint` module. Several endpoints were tested and the results are stored in [pylint.txt](https://github.com/CunningNobleman/library/blob/main/pylint_report.txt).
