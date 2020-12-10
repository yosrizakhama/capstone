from flask import request, jsonify, abort
from sqlalchemy import exc
import json
from models import app, Movie, Actor, db, ActorMovie
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    def test_data_actor(data):
        if 'name' not in data:
            abort(422)
        if 'genre' not in data:
            abort(422)
        if 'age' not in data:
            abort(422)
        if data.get('name') is None:
            abort(400)
        if data.get('genre') is None:
            abort(400)
        if data.get('age') is None:
            abort(400)

    def test_data_movie(data):
        if 'title' not in data:
            abort(422)
        if 'date' not in data:
            abort(422)
        if data.get('title') is None:
            abort(400)
        if data.get('date') is None:
            abort(400)

    @app.route('/', methods=['GET'])
    def salut():
        return "app running ok "
###

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            list_actors = Actor.query.all()
            actors_res = [act.__repr__() for act in list_actors]
        except:
            abort(404)
        return jsonify({
            "success": True,
            "code": 200,
            "message": "ACTORS DETAILS OK",
            "actors": actors_res,
            "nbr_actors": len(actors_res)
        })

#
    @app.route('/actors', methods=['POST'])
    @requires_auth('put:actors')
    def add_actors(payload):
        try:
            data = request.get_json()
        except:
            abort(405)
        if data is not None:
            n = data['name']
            a = data['age']
            g = data['genre']
            actor = Actor(name=n, age=a, genre=g)
            test_data_actor(data)
        else:
            abort(405)
        actor.insert()
        print(data)
        return jsonify({
            "success": True,
            "code": 200,
            "message": data['name']+" ADDED OK",
            "actors": [actor.__repr__()]
        })

#
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actors(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == int(id)).one_or_none()
        except:
            abort(405)
        data = request.get_json()
        if data is not None and actor is not None:
            test_data_actor(data)
            actor.name = data['name']
            actor.age = int(data['age'])
            actor.genre = data['genre']
            actor.update()
        else:
            abort(405)
        return jsonify({
            "success": True,
            "code": 200,
            "message": "UPDATE OK",
            "id": id,
            "actor": actor.__repr__()
        })

#
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == int(id)).one_or_none()
            actor.delete()
        except:
            abort(404)
        return jsonify({
            "success": True,
            "code": 200,
            "message": "DELETE OK",
            "id": id
        })

#
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            list_movies = Movie.query.all()
            movies_res = [act.__repr__() for act in list_movies]
        except:
            abort(404)
        return jsonify({
            "success": True,
            "code": 200,
            "message": "MOVIES DETAILS OK",
            "movies": movies_res,
            "nbr_movies": len(movies_res)
        })

#
    @app.route('/movies', methods=['POST'])
    @requires_auth('put:movies')
    def add_movies(payload):
        try:
            data = request.get_json()
        except:
            abort(405)
        if data is not None:
            test_data_movie(data)
            movie = Movie(title=data['title'], date=data['date'])
        else:
            abort(405)
        movie.insert()
        return jsonify({
            "success": True,
            "code": 200,
            "message": data['title']+" ADDED OK",
            "movies": [movie.__repr__()]
        })

#
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movies(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == int(id)).one_or_none()
        except:
            abort(405)
        data = request.get_json()
        if data is not None and movie is not None:
            test_data_movie(data)
            movie.title = data['title']
            movie.date = data['date']
            movie.update()
        else:
            abort(405)
        return jsonify({
            "success": True,
            "code": 200,
            "message": "UPDATE OK",
            "id": id,
            "movie": movie.__repr__()
        })

#
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == int(id)).one_or_none()
            movie.delete()
        except:
            abort(404)
        return jsonify({
            "success": True,
            "code": 200,
            "message": "DELETE OK",
            "id": id
        })

#
    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movie_actors')
    def get_movies_act(payload, id):
        try:
            connection = db.engine.connect()
            select = "select * from actormovie where movie_id="
            result = connection.execute(select+str(id)).fetchall()
            movies_res = []
            if result == []:
                abort(404)
            for mv_act in result:
                querie = Actor.query
                act = querie.filter(Actor.id == mv_act.actor_id).one_or_none()
                movies_res.append(act.__repr__())
        except:
            abort(404)
        return jsonify({
            "success": True,
            "code": 200,
            "message": "MOVIES DETAILS OK",
            "movies": movies_res,
            "nbr_movies": len(movies_res)
        })

#
    @app.route('/movies/<int:id>', methods=['POST'])
    @requires_auth('add:actors_movie')
    def add_actor_movies(payload, id):
        try:
            data = request.get_json()
            if data is not None:
                connection = db.engine.connect()
                select = "select * from actormovie where movie_id="
                select_q = select+str(id)+" and actor_id="+str(data['id'])
                result = connection.execute(select_q).fetchall()
                if len(result) == 0:
                    ins = ActorMovie.insert()
                    movies_actor = ins.values(actor_id=data['id'], movie_id=id)
                    db.engine.execute(movies_actor)
                else:
                    abort(405)
            else:
                abort(405)
        except:
            abort(405)
        return jsonify({
            "success": True,
            "code": 200,
            "message": " ADDED OK",
            "movies": id
        })

#
    @app.route('/movie_actors/<int:id>', methods=['DELETE'])
    @requires_auth('del:actors_movie')
    def del_actor_movies(payload, id):
        try:
            mov_act = ActorMovie.delete().where('actormovie.movie_id' == id)
            db.engine.execute(mov_act)
        except:
            abort(404)
        return jsonify({
            "success": True,
            "code": 200,
            "message": " DELETED OK",
            "movies": id
        })
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
