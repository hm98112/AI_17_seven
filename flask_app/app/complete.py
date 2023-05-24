from flask import Blueprint, render_template, request, current_app
import psycopg2

bp = Blueprint('complete', __name__, url_prefix='/')

#"/complete" url 접근 함수
@bp.route('/complete', methods=['POST', 'GET'])
def complete():
    
    current_app.config['attraction_price'] = request.form.get('attraction-price', 0)  # 선택된 투어 가격 데이터 가져오기
    # current_app.config['hotelTotalPrice'] = request.form.get('hotelTotalPrice', 0)  # 선택된 투어 가격 데이터 가져오기
    
    #정수로 변환
    attraction_price2 = int( str(current_app.config['attraction_price']).replace('₩', '').replace(',', ''))
    hotel_price2 = int( str(current_app.config['hotel_price']).replace('₩', '').replace(',', ''))
    hotelTotalPrice2 = int( str(current_app.config['hotelTotalPrice']).replace('₩', '').replace(',', ''))
    air_price2 = int( str(current_app.config['air_price']).replace('₩', '').replace(',', ''))
    
    #전체 가격 계산
    total_price = (attraction_price2 + hotelTotalPrice2 + air_price2) * int(current_app.config['count_people'])
    total_price = "₩{:,}".format(total_price)
    
    return render_template('complete.html', attraction_price=current_app.config['attraction_price'],hotel_price = current_app.config['hotel_price'] ,hotelTotalPrice = current_app.config['hotelTotalPrice'], air_price = current_app.config['air_price'], total_price = total_price, count_people=current_app.config['count_people'])