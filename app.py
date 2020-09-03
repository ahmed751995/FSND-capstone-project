import os, sys
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from database.models import setup_db, Actor, Movie, Show, db

sys.path.append(os.getcwd())

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                        'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response


@app.route('/actors')
def actors():
    try:
        actors = Actor.query.all()
        formated_actors = [actor.formate() for actor in actors]
        
        return jsonify({
        'success': True,
        'actors': formated_actors
        })
    
    except Exception:
        db.session.rollback()
        abort(404)
    finally:
        db.session.close()
        
        
@app.route('/movies')
def movies():
    try:
        movies = Movie.query.all()
        formated_movies = [movie.formate() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formated_movies
        })
    except Exception:
        db.session.rollback()
        abort(404)

    finally:
        db.session.close()



@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie == None:
            raise
        
        movie.delete()
        
        return jsonify({
            'success': True,
            'id': movie_id
        })
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor == None:
            raise

        actor.delete()

        return jsonify({
            'success': True,
            'id': actor_id
        })
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

@app.route('/movies', methods=['POST'])
def post_movie():
    try:
        body = request.get_json()
        if 'title' not in body:
            raise
        
        new_movie = Movie(title=body.get('title'),
                          release_date=body.get('release_date'))
        new_movie.insert()
        return jsonify({
            'success': True,
            'id': new_movie.id
        })
    
    except Exception:
        db.session.rollback()
        abort(400)
    finally:
        db.session.close()

        
@app.route('/actors', methods=['POST'])
def post_actor():
    try:
        body = request.get_json()
        if 'name' not in body:
            raise
        
        new_actor = Actor(name=body.get('name'),
                          age=body.get('age'),
                          gender=body.get('gender'))
        new_actor.insert()
        return jsonify({
            'success': True,
            'id': new_actor.id
        })
    
    except Exception:
        db.session.rollback()
        abort(400)
    finally:
        db.session.close()
    

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
def patch_movie(movie_id):
    try:
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        
        if movie == None:
            raise

        if 'title' in body:
            movie.title = body.get('title')

        if 'release_date' in body:
            movie.release_date = body.get('release_date')

        movie.update()

        return jsonify({
            'success': True
        })
    except Exception:
        db.session.rollback()
        abort(404)
    finally:
        db.session.close()


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
def patch_actor(actor_id):
    try:
        body = request.get_json()

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        
        if actor == None:
            raise

        if 'name' in body:
            actor.name = body.get('name')

        if 'age' in body:
            actor.age = body.get('age')

        if 'gender' in body:
            actor.gender = body.get('gender')

        actor.update()

        return jsonify({
            'success': True
        })
    except Exception:
        db.session.rollback()
        abort(404)
    finally:
        db.session.close()



        
    

if __name__ == '__main__':
    app.run(debug=True)



@app.errorhandler(404)
def not_found(error):
    return (jsonify({'success': False, 'error': 404,
                     'message': 'resource not found'}), 404)

@app.errorhandler(422)
def unprocessable(error):
    return (jsonify({'success': False, 'error': 422,
                     'message': 'unprocessable'}), 422)

@app.errorhandler(400)
def bad_request(error):
    return (jsonify({'success': False, 'error': 400,
                     'message': 'bad request'}), 400)

@app.errorhandler(500)
def bad_request(error):
    return (jsonify({'success': False, 'error': 500,
                     'message': 'internal server error'}), 500)
