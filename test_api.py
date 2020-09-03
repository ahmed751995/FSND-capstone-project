import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from database.models import setup_db, Actor, Movie, Show


class castingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "castingAgency_test"
        self.database_path = "postgres:///" + self.database_name
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_422_delete_movie(self):
        res = self.client().delete('/movies/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_422_delete_actor(self):
        res = self.client().delete('/actors/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_post_movie(self):
        movie = {"title": "jumanji", "release_date":"3-2-2021"}
        
        res = self.client().post('/movies', json=movie)
        data = json.loads(res.data)
        posted_movie = Movie.query.filter(Movie.id == data['id']).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(posted_movie.id)

    def test_400_post_movie(self):
        res = self.client().post('/movies', json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

        
    def test_post_actor(self):
        actor = {"name": "saif", "age": 18, "gender": "male"}
        
        res = self.client().post('/actors', json=actor)
        data = json.loads(res.data)
        posted_actor = Actor.query.filter(Actor.id == data['id']).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(posted_actor.id)


    def test_400_post_actor(self):
        res = self.client().post('/actors', json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_patch_movie(self):
        movie = {"title": "rush hour"}
        
        res = self.client().patch('/movies/2', json=movie)
        data = json.loads(res.data)
        patched_movie = Movie.query.filter(Movie.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(patched_movie.title, 'rush hour')

    def test_404_patch_movie(self):        
        res = self.client().patch('/movies/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    def test_patch_actor(self):
        actor = {"age": 40}
        
        res = self.client().patch('/actors/2', json=actor)
        data = json.loads(res.data)
        patched_actor = Actor.query.filter(Actor.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(patched_actor.age, 40)
    
    def test_404_patch_actor(self):        
        res = self.client().patch('/actors/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
