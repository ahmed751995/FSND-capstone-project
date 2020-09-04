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

        self.assistant_header = {
  'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRjeVJFQ1RmTjlabUF4c3I2TEV6SCJ9.eyJpc3MiOiJodHRwczovL2FobWVkNzUxOTk1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjMwOWIwZGQyZjFjZDAwMzdlZmM4NGQiLCJhdWQiOiJjYXNpbmdBZ2VuY3kiLCJpYXQiOjE1OTkyNTQzOTAsImV4cCI6MTU5OTI2MTU5MCwiYXpwIjoiaWNMQ01iOThrR3l6RGU2dUZnN1Z4VG9ySGRqSUxWR1QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.g_W8lsN4lGHQDzbCA1JISTDiYd4TzQn5NsBSR1I0GeZS6PkmkOzYjH99Hv0JuMKQuE36g_Uzym6NKSh87AcEdcy5nMXdg1ANJ6caHbAV8x5_mt4uzwgWi_yRXL2vpWqiJ9ilio2UF3XNVrApvg_ERIL1GxJ0-ZeUYOY_bKj-gSsQlBcQBqL74YSYdRyB42xxFts-x07rWMXGoHWOkZWq_sJgWgPwr2Wuq2OnR-M3IgzFv672My0tVZGS5B_yo-F7yDnRrn9AQWgAVCa-hIB8TgRi8tuTuilGoUTFI6ujsPhVPMGU6F3hUWY1e5VflQ7lR6v1tRkxqiICei7QiZ9hnQ'
}

        self.director_header = {
  'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRjeVJFQ1RmTjlabUF4c3I2TEV6SCJ9.eyJpc3MiOiJodHRwczovL2FobWVkNzUxOTk1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjMwOWJlZDY4ZGU5OTAwMzc0NmVlMTYiLCJhdWQiOiJjYXNpbmdBZ2VuY3kiLCJpYXQiOjE1OTkyNTQ3MTUsImV4cCI6MTU5OTI2MTkxNSwiYXpwIjoiaWNMQ01iOThrR3l6RGU2dUZnN1Z4VG9ySGRqSUxWR1QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.TK70j3ly4hQVByQDlPQyWdt5WpkKgWEd_3qpLCKyIef28LBXR5ZehPkxv7TUELWDiYFuJILeaa8jXaTXzN-lM2mQxFAzGoSs--hbWNGD6WN4CmOzgtEhugl3O0yUJfXXhRNO4-3RVBfdGf2RvxbcOl-KyF8o6Wbd6wrJxzIZLq4qyHdFf_LtC9m-mcvhScikrQwD4S_kd01RKT1H7F2n1e-q7LJHHucWGnK4E8kjpMH46MZJ3LxIh1ANc2V9_TenSjIgSq-PW7NBVBmovttsVXlIUaxMT3aWAk_hY8MwOSBx6AeJfms5aHvZKmCbamLzlC6KpEdKy_3QV5OVspoXbA'
}
       

        self.producer_header = {
  'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRjeVJFQ1RmTjlabUF4c3I2TEV6SCJ9.eyJpc3MiOiJodHRwczovL2FobWVkNzUxOTk1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjUyNDExN2U5ZWY1ZjAwNjdiNjQyOGUiLCJhdWQiOiJjYXNpbmdBZ2VuY3kiLCJpYXQiOjE1OTkyNTQzMTQsImV4cCI6MTU5OTI2MTUxNCwiYXpwIjoiaWNMQ01iOThrR3l6RGU2dUZnN1Z4VG9ySGRqSUxWR1QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.Jn9FWMNxlTcr-VZl32m_TwMMJ1bQJhUxgfna8jcsnxt3sLQhMw9Y25ObQ9tJTe8_LVkdIp-ex0g-t_B8QGokB10pOjnCfh66yvioeA2QHkO-Nr0AnvQbFATwOtuTM5SU2_tTjstFAEUc8RXRhNs4_r4JckSzEuLK_lHNCPH9MmTWV3bCokluZjELUM9-yD_YTqZeEsl2FTXxjjcyQmq7BQm2vTWkACE1oL39OuhAZGg3f_K4_qWX4AxfRWyeiVcAGGeXGFCvPS8vjzuQSKbobn0YxtWbkGn0_UCxyfP9Z1jPudon42NwsV6P6Mz04r9McNrR3jd1U5uaPWh8xmHR2g'
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
