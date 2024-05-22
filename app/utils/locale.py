from flask import request

def get_locale():
    return request.accept_languages.best_match([ 'en', 'nl' ])
