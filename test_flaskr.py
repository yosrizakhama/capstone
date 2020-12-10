import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import app, Movie, Actor, db, ActorMovie, database_path
from flask import Flask
from app import APP


token = os.environ['TOKENTEST']


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        # self.database_path = os.environ['DATABASE_TEST_PATH']
        self.exec_prod = token
        app.config['TESTING'] = True
        self.client = self.app.test_client
        self.new_actor = {
            "name": "ADEL IMEM",
            "age": 79,
            "genre": "M"
        }
        self.update_actor = {
            "name": "Leonardo De Caprio",
            "age": 65,
            "genre": "M"
        }
        self.new_movie = {
            "title": "Movie Test",
            "date": "2020-12-10"
        }
        self.update_movie = {
            "title": "A movie updated informations",
            "date": "20201212"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer '+self.exec_prod})
        self.assertEqual(res.status_code, 200)

    def test__not_get_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization': 'Bearer 1234'})
        self.assertEqual(res.status_code, 401)

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer ' + self.exec_prod})
        self.assertEqual(res.status_code, 200)

    def test__not_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization':
                                                    'Bearer 1234'})
        self.assertEqual(res.status_code, 401)

    def test_get_actorsmovie(self):
        res = self.client().get('/movies/1',
                                headers={'Authorization':
                                         'Bearer ' + self.exec_prod})
        self.assertEqual(res.status_code, 200)

    def test__not_get_actorsmovie(self):
        res = self.client().get('/movies/0',
                                headers={'Authorization':
                                         'Bearer ' + self.exec_prod})
        self.assertEqual(res.status_code, 404)

# Post end points
    def test_add_actors(self):
        res = self.client().post('/actors',
                                 headers={'Authorization':
                                          'Bearer ' + self.exec_prod},
                                 json=self.new_actor)
        self.assertEqual(res.status_code, 200)

    def test__not_add_actors(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer 1234'},
                                 json=self.new_actor)
        self.assertEqual(res.status_code, 401)

    def test_add_movies(self):
        res = self.client().post('/movies',
                                 headers={'Authorization':
                                          'Bearer ' + self.exec_prod},
                                 json=self.new_movie)
        self.assertEqual(res.status_code, 200)

    def test__not_add_movies(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer 1234'},
                                 json=self.new_movie)
        self.assertEqual(res.status_code, 401)

    def test_add_actorsmovie(self):
        res = self.client().post('/movies/5',
                                 headers={'Authorization':
                                          'Bearer ' + self.exec_prod},
                                 json={"id": 1})
        self.assertEqual(res.status_code, 200)

    def test__not_add_actorsmovie(self):
        res = self.client().post('/movies/5',
                                 headers={'Authorization': 'Bearer 1234'},
                                 json={"id": 1})
        self.assertEqual(res.status_code, 401)

# PATCH end points ###
    def test_update_actors(self):
        res = self.client().patch('/actors/1',
                                  headers={'Authorization':
                                           'Bearer ' + self.exec_prod},
                                  json=self.update_actor)
        self.assertEqual(res.status_code, 200)

    def test__not_update_actors(self):
        res = self.client().patch('/actors/1',
                                  headers={'Authorization': 'Bearer 1234'},
                                  json=self.update_actor)
        self.assertEqual(res.status_code, 401)

    def test_update_movies(self):
        res = self.client().patch('/movies/1',
                                  headers={'Authorization':
                                           'Bearer ' + self.exec_prod},
                                  json=self.update_movie)
        self.assertEqual(res.status_code, 200)

    def test__not_update_movies(self):
        res = self.client().patch('/movies/1',
                                  headers={'Authorization': 'Bearer 1234'},
                                  json=self.update_movie)
        self.assertEqual(res.status_code, 401)

# DELETE end points ###
    def test_del_actors(self):
        res = self.client().delete('/actors/6',
                                   headers={'Authorization':
                                            'Bearer ' + self.exec_prod},
                                   json=self.new_actor)
        self.assertEqual(res.status_code, 200)

    def test__not_del_actors(self):
        res = self.client().delete('/actors/6',
                                   headers={'Authorization': 'Bearer 1234'},
                                   json=self.new_actor)
        self.assertEqual(res.status_code, 401)

    def test_del_movies(self):
        res = self.client().delete('/movies/6',
                                   headers={'Authorization':
                                            'Bearer ' + self.exec_prod},
                                   json=self.new_movie)
        self.assertEqual(res.status_code, 200)

    def test__not_del_movies(self):
        res = self.client().delete('/movies/6',
                                   headers={'Authorization': 'Bearer 1234'},
                                   json=self.new_movie)
        self.assertEqual(res.status_code, 401)

    def test_del_actorsmovie(self):
        res = self.client().delete('/movie_actors/5',
                                   headers={'Authorization':
                                            'Bearer ' + self.exec_prod},
                                   json={"id": 1})
        self.assertEqual(res.status_code, 200)

    def test__not_del_actorsmovie(self):
        res = self.client().delete('/movie_actors/1',
                                   headers={'Authorization': 'Bearer 1234'},
                                   json={"id": 1})
        self.assertEqual(res.status_code, 401)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
