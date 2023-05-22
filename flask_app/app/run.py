from flask import Flask
import attraction

app = Flask(__name__)


app.register_blueprint(attraction.bp)

    
@app.route('/')
def index():
    return 'bbb'




if __name__ == '__main__':
    app.run(host= '0.0.0.0')