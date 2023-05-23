from flask import Blueprint, render_template, request
import psycopg2

bp = Blueprint('complete', __name__, url_prefix='/')



@bp.route('/complete', methods=['POST', 'GET'])
def complete():
    attraction_price = request.form.get('attraction-price', 0)  # 선택된 투어 가격 데이터 가져오기
    hotel_price = request.form.get('hotel-price', 0)
    air_price = request.form.get('air_price', 0)
    count_people = request.form.get('count_people', 0)
    attraction_price2 = int( str(attraction_price).replace('₩', '').replace(',', ''))
    hotel_price2 = int( str(hotel_price).replace('₩', '').replace(',', ''))
    air_price2 = int( str(air_price).replace('₩', '').replace(',', ''))
    # total_price = (attraction_price2 + hotel_price2 + air_price2)
    total_price = (attraction_price2 + hotel_price2 + air_price2) * int(count_people)
    total_price = "₩{:,}".format(total_price)
    return render_template('complete.html', attraction_price=attraction_price, hotel_price = hotel_price, air_price=air_price, total_price = total_price, count_people=count_people)