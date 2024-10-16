# SQL Movie Database

### Goal


---

### movie_db.py

SQL queries that answer 12 questions.

### Database

The database you are provided with is an SQLite database, stored in the file `cs1656-public.db`. The schema of the database is as follows:
* Actors (aid, fname, lname, gender)  
* Movies (mid, title, year, rank)  
* Directors (did, fname, lname)  
* Cast (aid, mid, role)  
* Movie_Director (did, mid)  


### Queries

SQL queries that provide answers for the following questions. Note that **actors** refers to both male and female actors, unless explicitly specified otherwise.

* **[Q01]** List all the actors (first and last name) who acted in at least one film in the 80s (1980-1990, both ends inclusive) and in at least one film in the 21st century (>=2000). Sort alphabetically, by the actor's last and first name.

* **[Q02]** List all the movies (title, year) that were released in the same year as the movie entitled `"Rogue One: A Star Wars Story"`, but had a better rank (Note: the higher the value in the *rank* attribute, the better the rank of the movie). Sort alphabetically, by movie title.  

* **[Q03]** List all the actors (first and last name) who played in a Star Wars movie (i.e., title like '%Star Wars%') in decreasing order of how many Star Wars movies they appeared in. If an actor plays multiple roles in the same movie, count that still as one movie. If there is a tie, use the actor's last and first name to generate a full sorted order. Sort alphabetically, by the number of movies (descending), the actor's last name and first name.  

* **[Q04]** Find the actor(s) (first and last name) who **only** acted in films released before 1990. Sort alphabetically, by the actor's last and first name.  

* **[Q05]** List the top 10 directors in descending order of the number of films they directed (first name, last name, number of films directed). For simplicity, feel free to ignore ties at the number 10 spot (i.e., always show up to 10 only). Sort alphabetically, by the number of films (descending), the actor's last name and first name.  

* **[Q06]** Find the top 10 movies with the largest cast (title, number of cast members) in decreasing order. Note: show all movies in case of a tie.  

* **[Q07]** Find the movie(s) whose cast has more actors than actresses (i.e., gender=Male vs gender=Female).  Show the title, the number of actors, and the number of actresses in the results. Sort alphabetically, by movie title. Hint: Make sure you account for the case of 0 actors or actresses in a movie.

* **[Q08]** Find all the actors who have worked with at least 7 different directors. Do not consider cases of self-directing (i.e., when the director is also an actor in a movie), but count all directors in a movie towards the threshold of 7 directors. Show the actor's first, last name, and the number of directors he/she has worked with. Sort in decreasing order of number of directors.

* **[Q09]** For all actors whose first name starts with a **B**, count the movies that he/she appeared in his/her debut year (i.e., year of their first movie). Show the actor's first and last name, plus the count. Sort by decreasing order of the count, then the first and last name.  

* **[Q10]** Find instances of nepotism between actors and directors, i.e., an actor in a movie and the director having the same last name, but a different first name. Show the last name and the title of the movie, sorted alphabetically by last name and the movie title.  

* **[Q11]** The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the *"co-acting"* graph. That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him have Bacon number 1; all actors who acted in the same film as some actor with Bacon number 1 have Bacon number 2, etc. List all actors whose Bacon number is 2 (first name, last name). Sort the results by the last and first name. You can familiarize yourself with the concept, by visiting [The Oracle of Bacon](https://oracleofbacon.org).  

* **[Q12]** Assume that the *popularity* of an actor is reflected by the average *rank* of all the movies he/she has acted in. Find the top 20 most popular actors (in descreasing order of popularity) -- list the actor's first/last name, the total number of movies he/she has acted, and his/her popularity score. For simplicity, feel free to ignore ties at the number 20 spot (i.e., always show up to 20 only).  

---

Here’s an improved version of your README file, tailored for GitHub to enhance clarity and structure:

SQL Movie Database

Project Overview

This project is designed to query a movie database to extract meaningful insights. You will use SQL to answer various questions about the data, which covers movies, actors, directors, and their roles. The database schema is outlined below, providing details on each table and its columns.

Files

	•	movie_db.py: This script contains the SQL queries to answer 12 specific questions about the movie database.
	•	cs1656-public.db: An SQLite database file with information on movies, actors, directors, and their respective relationships.

Database Schema

The provided SQLite database contains the following tables:

	•	Actors: Contains information about actors, including:
	•	aid (Actor ID)
	•	fname (First name)
	•	lname (Last name)
	•	gender
	•	Movies: Details of each movie, including:
	•	mid (Movie ID)
	•	title (Title of the movie)
	•	year (Release year)
	•	rank (Rating)
	•	Directors: Information about directors:
	•	did (Director ID)
	•	fname (First name)
	•	lname (Last name)
	•	Cast: Maps actors to movies and their roles:
	•	aid (Actor ID)
	•	mid (Movie ID)
	•	role (Role in the movie)
	•	Movie_Director: Links movies to directors:
	•	did (Director ID)
	•	mid (Movie ID)

Queries

This project answers the following questions using SQL:

	1.	Example Query 1: Describe what it does…
	2.	Example Query 2: Describe what it does…

(Continue listing queries in a similar format for clarity.)

How to Use

	1.	Database Setup: Ensure you have SQLite installed to interact with cs1656-public.db.
	2.	Running Queries: Open movie_db.py in your preferred IDE or text editor to review the SQL queries. You can run these queries directly within SQLite to get the results.
	3.	Modify Queries: Feel free to modify the queries in movie_db.py to explore additional insights from the database.

Requirements

	•	SQLite: You need to have SQLite installed to access and query the database file.

License

Specify your license here, if any (e.g., MIT License).

Contributing

Contributions are welcome! Please fork the repository and submit a pull request if you would like to improve the project.

This revised structure makes the README more user-friendly, improving readability and making it easier for users to understand the project and its components. Let me know if you’d like further adjustments or additions! ￼









