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

        self.assistant_token = 'Bearer ' + os.environ['assistant']
        self.director_token = 'Bearer ' + os.environ['director']
        self.producer_token = 'Bearer ' + os.environ['producer']
        
        self.assistant_header = {
            'Authorization': self.assistant_token
        }

        self.director_header = {
            'Authorization': self.director_token
        }
        
        self.producer_header = {
            'Authorization': self.producer_token
        }
        

        
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
        header = self.producer_header
        res = self.client().get('/actors', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        header = self.producer_header
        res = self.client().get('/movies', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_delete_movie(self):
        header = self.producer_header
        res = self.client().delete('/movies/1', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_422_delete_movie(self):
        header = self.producer_header
        res = self.client().delete('/movies/100', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        header = self.producer_header
        res = self.client().delete('/actors/1', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_422_delete_actor(self):
        header = self.producer_header
        res = self.client().delete('/actors/100', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_post_movie(self):
        header = self.producer_header
        movie = {"title": "jumanji", "release_date":"3-2-2021"}
        
        res = self.client().post('/movies', json=movie, headers=header)
        data = json.loads(res.data)
        posted_movie = Movie.query.filter(Movie.id == data['id']).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(posted_movie.id)

    def test_400_post_movie(self):
        header = self.producer_header
        movie = {"release_date":"3-2-2021"}
        res = self.client().post('/movies', json=movie, headers=header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

        
    def test_post_actor(self):
        actor = {"name": "saif", "age": 18, "gender": "male"}
        header = self.producer_header
        
        res = self.client().post('/actors', json=actor, headers=header)
        data = json.loads(res.data)
        posted_actor = Actor.query.filter(Actor.id == data['id']).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(posted_actor.id)


    def test_400_post_actor(self):
        header = self.producer_header
        res = self.client().post('/actors', json={}, headers=header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_patch_movie(self):
        movie = {"title": "rush hour"}
        header = self.producer_header
        res = self.client().patch('/movies/2', json=movie, headers=header)
        data = json.loads(res.data)
        patched_movie = Movie.query.filter(Movie.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(patched_movie.title, 'rush hour')

    def test_404_patch_movie(self):
        header = self.producer_header
        res = self.client().patch('/movies/100', headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    def test_patch_actor(self):
        header = self.producer_header
        actor = {"age": 40}
        
        res = self.client().patch('/actors/2', json=actor, headers=header)
        data = json.loads(res.data)
        patched_actor = Actor.query.filter(Actor.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(patched_actor.age, 40)
    
    def test_404_patch_actor(self):
        header = self.producer_header
        res = self.client().patch('/actors/100', headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)



    #test roles
    # !hint : i already tested producer on the above test cases so 
    # i will test only the assistant and director

    #assistant tests
    def test_get_actors(self):
        header = self.assistant_header
        res = self.client().get('/actors', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))


    def test_delete_movie(self):
        header = self.assistant_header
        res = self.client().delete('/movies/1', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    #director test
    def test_delete_actor(self):
        header = self.director_header
        res = self.client().delete('/actors/1', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)


    def test_delete_movie(self):
        header = self.director_header
        res = self.client().delete('/movies/1', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)



        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
