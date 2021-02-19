from flask import jsonify

from controllers.auth import Auth
from controllers.candidates import Candidates
from controllers.resume import Resume
from exceptions import TinyHRError
from genesis import create_app

# Initiate Flask App
app = create_app()
# Small tweak to accept leading slashes in urls.
app.url_map.strict_slashes = False
# Registering Controllers (Blueprints)
app.register_blueprint(Auth)
app.register_blueprint(Candidates)
app.register_blueprint(Resume)


# Error Handlers
@app.errorhandler(TinyHRError)
def exception_handler(error):
    response = jsonify(error.serialize())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def does_not_exist_handler(_error):
    response = jsonify({
        "error": 'Not Found'
    })
    return response, 404


if __name__ == '__main__':
    app.run()
