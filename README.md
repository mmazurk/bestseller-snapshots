
# Capstone Project

<br>

Bestseller Snapshots allows a user to find new books to read based on bestseller lists and book reviews from the past. Once the user has a list, they can explore more information about the books and save them to their landing page.

<br>

## Database Design

Here is the database design that can be pasted into: 
https://app.quickdatabasediagrams.com/#/

	users 
	--
	user_id int PK
	email text
	username text
	password text
	image_url text
	bio text

	lists
	--
	list_id int PK
	list_name text
	list_name_encoded text
	oldest_published_date date
	newest_published_date date

	user_lists
	--
	user_lists_id int PK
	list_id int FK >- lists.list_id
	user_id int FK >- users.user_id

	user_books
	--
	note_id int PK
	text text
	user_id int FK >- users.user_id
	book_id int FK >- books.book_id

	books
	--
	book_id int PK
	title text
	author text
	image_link text
