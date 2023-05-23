from flask import Flask
import attraction
import complete
import hotel
import airline
from flask import Flask, redirect

app = Flask(__name__)


app.register_blueprint(attraction.bp)
app.register_blueprint(complete.bp)
app.register_blueprint(hotel.bp)
app.register_blueprint(airline.bp)



@app.route('/')
def index():
    return redirect('/first')

@app.route('/first')
def first():
    return 'bbb'




if __name__ == '__main__':
    app.run(host= '0.0.0.0')