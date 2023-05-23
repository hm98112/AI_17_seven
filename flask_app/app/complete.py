from flask import Blueprint, render_template, request
import psycopg2

bp = Blueprint('complete', __name__, url_prefix='/')



@bp.route('/complete', methods=['POST', 'GET'])
def complete():
    attraction_price = request.form.get('attraction-price', 0)  # 선택된 투어 가격 데이터 가져오기
    hotel_price = request.form.get('hotel-price', 0)
    return render_template('complete.html', attraction_price=attraction_price, hotel_price = hotel_price)