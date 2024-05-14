#!/usr/bin/python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
from flask import Flask
#from models import storage
storage = __import__("models").storage
from api.v1.views import app_views
#current_dir = os.path.dirname(os.path.abspath(__file__))
#project_root = os.path.abspath(os.path.join(current_dir, '../../'))
#sys.path.insert(0, project_root)

# Create a variable app, instance of Flask
app = Flask(__name__)
#print(storag.all())
# register the blueprint app_views to your Flask instance app
@app.register_blueprint(app_views, url_prefix='/api/vi')
# declare a method to handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_storage(exception):
    print("teardown initiated")
    if exception:
        print(exception)
    storage.close()

if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    port = os.getenv("HBNB_API_PORT", default="5000")

    app.run(host=host, port=port, threaded=True)
