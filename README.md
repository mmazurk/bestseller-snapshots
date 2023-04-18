
# Capstone Project

<br>

Bestseller Snapshots allows a user to find new books to read based on bestseller lists and book reviews from the past. Once the user has a list, they can explore more information about the books and create their own customized reading lists.

<br>

## Database Design

Here is the database design that can be pasted into: 
https://app.quickdatabasediagrams.com/#/

    users 
    --
    user_id int PK
    email text
    username text
    image_url text
    bio text
    password text

    notes
    --
    note_id int PK
    text text
    timestamp datetime
    user_id int FK >- users.user_id
    book_id int FK >- books.book_id

    books
    --
    book_id int PK
    title text
    author text
    image_link text
    review_link text
    amazon_link text
    description text 
    publisher text
    user_id int FK >- users.user_id

    nyt_lists
    --
    list_id int PK
    list_name text
    oldest_published_date date
    newest_published_date date
    user_id int FK >- users.user_id
    book_id int FK >- books.book_id

    user_lists
    --
    list_id int PK
    list_name text
    user_id int FK >- users.user_id
    book_id int FK >- books.book_id
