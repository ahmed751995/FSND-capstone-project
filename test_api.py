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

       

        self.producer_header = {
  'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRjeVJFQ1RmTjlabUF4c3I2TEV6SCJ9.eyJpc3MiOiJodHRwczovL2FobWVkNzUxOTk1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjUyNDExN2U5ZWY1ZjAwNjdiNjQyOGUiLCJhdWQiOiJjYXNpbmdBZ2VuY3kiLCJpYXQiOjE1OTkyNDY5NzUsImV4cCI6MTU5OTI1NDE3NSwiYXpwIjoiaWNMQ01iOThrR3l6RGU2dUZnN1Z4VG9ySGRqSUxWR1QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.l5HN4jn2KvULEyCNbN7gGPfEV57uLbtecV1VoDCxIqTEvDTb35jgZRyoqZpUbG-dcPWRsDRSYv2F7Suxf7L69rveDsOIC2TZ786P0_sQcE7QNnMktFnkQnDnMO5BopZua2cpbyTz9fX7N7ylcwoVWwpNsjHrf_lgWf6g-zRh7ljSFjtTQny19hOzDaggFen2LPqDccxcLV05UT4dXv0Fai5I7rK58GINK_bVZo5k2NP5f8jzlBnfyDFnT95FxUdiONkjlVSCqFVGiubKGh2VD3YxYfa8XsSyXe33pXD9s4yxfPKegPX24zdMTCnJVawyMLoKYNwn8MhakUcXVvTElg'
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
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
