from flask import Flask
import attraction
import complete
import hotel
import airline
from flask import Flask, redirect, current_app, render_template

app = Flask(__name__)


#글로벌 변수 선언 설정된 변수를 사용하기 위해선 app.config를 통해 접근

with app.app_context():
    current_app.config['count_people'] = 0
    current_app.config['air_price'] = 0
    current_app.config['hotel_price'] = 0
    current_app.config['attraction_price'] = 0
    current_app.config['hotelTotalPrice'] = 0
 

#각 페이지별 블루 프린트 불러오기
app.register_blueprint(attraction.bp)
app.register_blueprint(complete.bp)
app.register_blueprint(hotel.bp)
app.register_blueprint(airline.bp)



@app.route('/')
def index():
    return redirect('/first')

@app.route('/first', methods=['POST','GET'])
def first():
    return render_template('first.html')


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
    