import sqlite3 as lite
import csv
import re
import pandas as pd
import argparse
import collections
import json
import glob
import math
import os
import requests
import string
import sqlite3
import sys
import time
import xml

#* Actors (aid, fname, lname, gender)
#* Movies (mid, title, year, rank)
#* Directors (did, fname, lname)
#* Cast (aid, mid, role)
#* Movie_Director (did, mid)

class Movie_db(object):
    def __init__(self, db_name):
        db_name: "cs1656-public.db"
        self.con = lite.connect(db_name)
        self.cur = self.con.cursor()

    #q0 is an example
    def q0(self):
        query = '''SELECT COUNT(*) FROM Actors'''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q1(self):
        # DONE
        # List all the actors (first and last name) who acted in at least one film in the 80s (1980-1990, both ends inclusive) and in at least one film in the 21st century (>=2000). Sort alphabetically, by the actor's last and first name.
        query = '''
            SELECT DISTINCT fname, lname
            FROM Actors
            WHERE aid IN (SELECT aid
                            FROM Cast
                            WHERE mid IN (SELECT mid
                                            FROM Movies
                                            WHERE year BETWEEN 1980 AND 1990))
            AND aid IN (SELECT aid
                        FROM Cast
                        WHERE mid IN (SELECT mid
                                        FROM Movies
                                        WHERE year >= 2000))
            ORDER BY lname, fname
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


    def q2(self):
        # DONE
        # List all the movies (title, year) that were released in the same year as the movie entitled "Rogue One: A Star Wars Story", but had a better rank (Note: the higher the value in the rank attribute, the better the rank of the movie). Sort alphabetically, by movie title.
        query = '''
            SELECT title, year
            FROM Movies
            WHERE year = (SELECT year
                            FROM Movies
                            WHERE title = "Rogue One: A Star Wars Story")
            AND rank > (SELECT rank
                            FROM Movies
                            WHERE title = "Rogue One: A Star Wars Story")
            ORDER BY title
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q3(self):
        # DONE
        # List all the actors (first and last name) who played in a Star Wars movie (i.e., title like '%Star Wars%') in decreasing order of how many Star Wars movies they appeared in. If an actor plays multiple roles in the same movie, count that still as one movie. If there is a tie, use the actor's last and first name to generate a full sorted order. Sort alphabetically, by the number of movies (descending), the actor's last name and first name.
        query = '''
            SELECT a.fname, a.lname, COUNT(distinct c.mid) AS num_movies
            FROM Actors a
            JOIN Cast c ON c.aid = a.aid
            JOIN Movies m ON m.mid = c.mid
            WHERE m.title LIKE '%Star Wars%'
            GROUP BY a.aid
            ORDER BY num_movies DESC, a.lname, a.fname
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


    def q4(self):
        # DONE
        # Find the actor(s) (first and last name) who only acted in films released before 1990. Sort alphabetically, by the actor's last and first name.
        query = '''
            SELECT a.fname, a.lname
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            WHERE m.year < 1990 AND a.aid NOT IN (
                SELECT a2.aid
                FROM Actors a2
                JOIN Cast c2 ON a2.aid = c2.aid
                JOIN Movies m2 ON c2.mid = m2.mid
                WHERE m2.year >= 1990
            )
            GROUP BY a.lname, a.fname;
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q5(self):
        # DONE
        # List the top 10 directors in descending order of the number of films they directed (first name, last name, number of films directed). For simplicity, feel free to ignore ties at the number 10 spot (i.e., always show up to 10 only). Sort alphabetically, by the number of films (descending), the actor's last name and first name.
        query = '''
            SELECT fname, lname, COUNT(distinct mid) AS num_movies
            FROM Directors
            JOIN Movie_Director ON Movie_Director.did = Directors.did
            GROUP BY Directors.did
            ORDER BY num_movies DESC, lname, fname
            LIMIT 10
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q6(self):
        # DONE
        # Find the top 10 movies with the largest cast (title, number of cast members) in decreasing order. Note: show all movies in case of a tie.
        query = '''
            SELECT m.title, COUNT(*) as num_cast
            FROM Movies m
            JOIN Cast c ON m.mid = c.mid
            GROUP BY m.mid
            HAVING num_cast >= (
                SELECT MIN(num_cast)
                FROM(
                    SELECT COUNT(*) as num_cast
                    FROM Movies m
                    JOIN Cast c ON m.mid = c.mid
                    GROUP BY m.mid
                    ORDER BY num_cast DESC, m.title
                    LIMIT 10
                )
            )
            ORDER BY num_cast DESC, m.title
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q7(self):
        # DONE
        # Find the movie(s) whose cast has more actors than actresses (i.e., gender=Male vs gender=Female). Show the title, the number of actors, and the number of actresses in the results. Sort alphabetically, by movie title. Hint: Make sure you account for the case of 0 actors or actresses in a movie.
        query = '''
            SELECT m.title,
                COUNT(CASE WHEN a.gender = 'Male' THEN 1 END) AS num_actors,
                COUNT(CASE WHEN a.gender = 'Female' THEN 1 END) AS num_actresses
            FROM Movies m
            JOIN Cast c ON c.mid = m.mid
            JOIN Actors a ON a.aid = c.aid
            GROUP BY m.mid
            HAVING COUNT(CASE WHEN a.gender = 'Male' THEN 1 END) > COUNT(CASE WHEN a.gender = 'Female' THEN 1 END)
            ORDER BY m.title ASC;
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q8(self):
        # DONE
        # Find all the actors who have worked with at least 7 different directors. Do not consider cases of self-directing (i.e., when the director is also an actor in a movie), but count all directors in a movie towards the threshold of 7 directors. Show the actor's first, last name, and the number of directors he/she has worked with. Sort in decreasing order of number of directors.
        query = '''
            SELECT a.fname, a.lname, COUNT(distinct md.did) AS num_directors
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            JOIN Movie_Director md ON m.mid = md.mid
            JOIN Directors d ON md.did = d.did AND d.fname <> a.fname AND d.lname <> a.lname
            GROUP BY a.aid, a.fname, a.lname
            HAVING COUNT(distinct md.did) >= 7
            ORDER BY num_directors DESC;
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


    def q9(self):
        # DONE
        # For all actors whose first name starts with a B, count the movies that he/she appeared in his/her debut year (i.e., year of their first movie). Show the actor's first and last name, plus the count. Sort by decreasing order of the count, then the first and last name.
        query = '''
            SELECT a.fname, a.lname, COUNT(distinct c.mid) AS num_movies
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            WHERE a.fname LIKE 'B%' AND m.year = (
                SELECT MIN(m2.year)
                FROM Movies m2
                JOIN Cast c2 ON c2.mid = m2.mid
                WHERE c2.aid = a.aid
            )
            GROUP BY a.aid
            ORDER BY num_movies DESC, a.fname, a.lname;
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q10(self):
        # DONE
        # Find instances of nepotism between actors and directors, i.e., an actor in a movie and the director having the same last name, but a different first name. Show the last name and the title of the movie, sorted alphabetically by last name and the movie title.
        query = '''
            SELECT a.lname, m.title
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            JOIN Movie_Director md ON m.mid = md.mid
            JOIN Directors d ON md.did = d.did
            WHERE a.lname = d.lname AND a.fname != d.fname
            ORDER BY a.lname, m.title
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q11(self):
        # DONE
        # The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the "co-acting" graph. That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him have Bacon number 1; all actors who acted in the same film as some actor with Bacon number 1 have Bacon number 2, etc. List all actors whose Bacon number is 2 (first name, last name). Sort the results by the last and first name. You can familiarize yourself with the concept, by visiting The Oracle of Bacon.
        # VIEW FOR ALL KEVIN BACON MOVIES
        self.cur.execute("DROP VIEW IF EXISTS bacon_movies")
        query = '''
            CREATE VIEW bacon_movies AS
            SELECT m.mid
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            WHERE a.lname = "Bacon"
            '''
        self.cur.execute(query)
        # VIEW FOR ACTORS WITH BACON NUMBER OF 1 (excluding kevin himself)
        self.cur.execute("DROP VIEW IF EXISTS bacon_num_1")
        query = '''
            CREATE VIEW bacon_num_1 AS
            SELECT a.aid
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            WHERE m.mid IN (SELECT mid FROM bacon_movies) AND NOT (a.lname = "Bacon")
        '''
        self.cur.execute(query)
        # VIEW THAT SELECTS ALL MOVIES THAT ACTORS FROM bacon_num_1 HAVE ACTED IN THAT KEVIN IS NOT IN(NOT bacon_movies)
        self.cur.execute("DROP VIEW IF EXISTS mov_without_kb")
        query = '''
            CREATE VIEW mov_without_kb AS
            SELECT m.mid
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            WHERE a.aid IN (SELECT * FROM bacon_num_1) AND NOT a.lname = "Bacon" AND NOT m.mid IN (
                SELECT mid FROM bacon_movies
            )
        '''
        self.cur.execute(query)
        query = '''
            SELECT DISTINCT a.fname, a.lname
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            WHERE m.mid IN (SELECT * FROM mov_without_kb) AND NOT a.lname = "Bacon" AND NOT m.mid IN (SELECT mid FROM bacon_movies) AND NOT a.aid in (SELECT * FROM bacon_num_1)
            ORDER BY a.lname, a.fname
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q12(self):
        # DONE
        # Assume that the popularity of an actor is reflected by the average rank of all the movies he/she has acted in. Find the top 20 most popular actors (in descreasing order of popularity) -- list the actor's first/last name, the total number of movies he/she has acted, and his/her popularity score. For simplicity, feel free to ignore ties at the number 20 spot (i.e., always show up to 20 only).
        query = '''
            SELECT a.fname, a.lname, COUNT(c.mid) AS num_movies, AVG(m.rank) AS popularity
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            GROUP BY a.aid, a.fname, a.lname
            ORDER BY popularity DESC
            LIMIT 20
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

if __name__ == "__main__":
    task = Movie_db("cs1656-public.db")
    rows = task.q0()
    print(rows)
    print()
    rows = task.q1()
    print(rows)
    print()
    rows = task.q2()
    print(rows)
    print()
    rows = task.q3()
    print(rows)
    print()
    rows = task.q4()
    print(rows)
    print()
    rows = task.q5()
    print(rows)
    print()
    rows = task.q6()
    print(rows)
    print()
    rows = task.q7()
    print(rows)
    print()
    rows = task.q8()
    print(rows)
    print()
    rows = task.q9()
    print(rows)
    print()
    rows = task.q10()
    print(rows)
    print()
    rows = task.q11()
    print(rows)
    print()
    rows = task.q12()
    print(rows)
    print()