
# Bestseller Snapshots

## Summary and DB Design

Bestseller Snapshots allows a user to navigate the New York Times Bestseller Lists in an innovative and interactive way. Rather than just viewing the current bestseller lists passively (and having to manually record or copy books to read) the user can browse multiple lists and favorites to a landing page. Users can also save favorite books, and the app will indicate to the user when they have done so. Most importantly, users can search besteller lists of the past -- extending as far back as the data allows -- and explore books they might have missed.

## Note to the Reader

I am obviously a new developer, so many of the methods I used in this application are based on my limited (but ever-growing) knowledge of how to develop applications so they are stable, maintanble, and extensible. If you happen to be reading this in the future (me, or someone else) be kind. 

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
	isbns_combined text
	title text
	author text
	description text
	image_url text

# Project Challenges

## **CHALLENGE #1** -- Avoiding Repeated API Calls

There are restrictions stated on the NYT website (listed here https://developer.nytimes.com/docs/books-product/1/overview) that say: " ... there are two rate limits per API: 500 requests per day and 5 requests per minute. You should sleep 12 seconds between calls to avoid hitting the per minute rate limit."

Because I was unable to use a caching solution (such as redis https://redis.io/), I solved this problem in two ways. First, I created a booklist.py object that only made a single API call but stored all the necessary information to generate the list of bestseller lists for users.

I also wrote two functions, one which pulled all of the list data from the API and a second function which created curated lists for me to present to the user.

	def __init__(self):

		self.data = self.get_data()
		self.fiction = self.make_list(fiction_list)
		self.nonfiction = self.make_list(nonfiction_list)
		self.exciting = self.make_list(exciting_list)
		self.business = self.make_list(business_list)
		self.graphic = self.make_list(graphic_list)
		self.childrens = self.make_list(childrens_list)

		non_categorized = [item['list_name'] for item in self.data if item['list_name'] not in all_categorized]
		self.other = self.make_list(non_categorized)

	def get_data(self):

		res = requests.get(f"{API_BASE_URL}lists/names.json", params={'api-key': key})
		data = res.json()
		dict_list = data['results']
		return dict_list

	def make_list(self, category_list):

		items = [item for item in self.data if item['list_name'] in category_list]
		return items

> __FUTURE ITERATION__: I am going to learn about caching services such as Reddis and then develop a method to store all different API calls that are required for the pages. This will allow the page to scale.

<br>

## **CHALLENGE #2** -- Storing and creating a unique identifer for books

Interestingly enough, the API does not allow me to call it and look up a specific book. This presented some problems for storing and retrieving books that users favorited. In addition, published books used to have isbn_10 numbers until 2011, at which point a new system was needed. The industry switched to isbn_13 numbers. Even with this change, most new books still assign books both numbers, but not all the time. 

To solve the first problem, I just saved all the relevant information about books as users favorited them. To solve the second problem, I created a new, unique id called `isbns_combined` that retrieved the primary isbn_10 and isbn_13 numbers from the API call and combined them into a single value. 

    __tablename__ = "books"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    isbns_combined = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))

> __FUTURE ITERATION__: I need to use automated repeated API calls and build a master list of all books on the NYT bestseller lists (rather than having limited information added when users save them). There is much more data on the books than I included in my site, and it might be useful to have that (for example, a buy link to different online bookstores).   

<br>

## **CHALLENGE #3** -- Using GET requests for all Python routes

To keep the pages simple and limit the scope of the project, I tried to limit use of AJAX and do most of the work GET requests to Python routes with embedded query parameters. I wasn't sure the best method to pass data between pages, but since the NYT bestseller lists are all public information, I chose to use GET requestsy:

Anchor tag with query embedded: 

	<a href="/book-results?list_name_encoded={{item.list_name_encoded}}" id="{{item.list_name_encoded}}"
	class=" btn btn-sm btn-primary mt-2">Go to List!</a>

The route:

	@app.route("/book-results")
	def show_list():
		"""search through book lists"""

		list_name_encoded = request.args.get('list_name_encoded')
		date = request.args.get('date')

		res = requests.get(
			f"{API_BASE_URL}lists/{date}/{list_name_encoded}.json", params={'api-key': key})
		data = res.json()
		display_name = data['results']['display_name']
		list_name_encoded = data['results']['list_name_encoded']
		published_date = data['results']['published_date']
		books = data['results']['books']

However, I ran into a problem when I tried to modify the list-search page so it picked up the date range in real-time (in input type="date") that the user wanted. I couldn't figure out how to embed this information into a GET request as a query parameter without using .js, so I had to do this: 

	// Add a click event listener to all the "Go to List!" links on the page

	$('#container-div').on('click', "a", function(event) {
		
		if ($(this).text() === "Go to List!") {

			event.preventDefault();
			const listNameEncoded = $(this).attr('id');
			console.log(listNameEncoded)
			const dateField = $('#' + listNameEncoded + '_date');
			console.log(dateField.val())
			const linkUrl = $(this).attr('href') + '&date=' + dateField.val();
			console.log(linkUrl)
		
			window.location.href = linkUrl;
		
		}

	});   

> __FUTURE ITERATION__: I need to figure out more consistent and robust way to pass data between my pages. Right now I have a mixture of GET requests using links and query parameters, POST requests using form data, and AJAX pulling information from the DOM and embedding it into a GET request using links and query parameters. 

<br>

# Future Iterations

I want to make these improvements before I push this to production and allow users to interact with it.

* __Improve the "My Saved Lists":__ Currently, the 'My Saved Lists' on the landing page is just a reminder to the user of the lists that they have liked in the past, and it doesn't include any information about the date ranges the user may have searched or liked. 

* __Use of AJAX on pages":__ The only page that uses JavaScript is the list-search page (as described above). In future iterations I could use AJAX on any of the pages where the user is allowed to "add" or "remove" a book/list to their favorites. 

* __Update of UI and Back End__: I was limited in this project to using only the tools that I had learned in my course, such as Flask. In future iterations, I may refactor the code to be more maintable by using a different technology. 

* __Increase Security__: I have not tested all the possible ways that users could try and break the site by manipulating the URLs or Javascript console, so this needs to be done in the future. 

