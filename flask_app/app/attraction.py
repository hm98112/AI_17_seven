from flask import Blueprint, render_template, request
import psycopg2

bp = Blueprint('index', __name__, url_prefix='/')



conn = psycopg2.connect(
    database="ai-17-seven",
    user="hm98112",
    password="123456!@#",
    host="34.64.57.43",
    port="5432"
)



@bp.route('/attraction', methods=['POST', 'GET'])
def index():
    
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT category FROM attraction")
    categories = cursor.fetchall()
    
    cursor.execute("SELECT name, category, score, time, price FROM attraction")
    rows = cursor.fetchall()
    
    cursor.close()
    
    hotel_price = str(request.form.get('hotel-price'))
    air_price = str(request.form.get('air_price'))
    count_people = str(request.form.get('count_people'))

    return render_template('attraction.html', categories=categories, results = rows[:10], hotel_price = hotel_price, air_price=air_price, count_people = count_people)

@bp.route('/attraction/price-selection', methods=['POST','GET'])
def price_selection():
    selected_category = request.form.get('attraction-category')
    att_order = request.form.get('order')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT category FROM attraction")
    categories = cursor.fetchall()

    hotel_price = request.form.get('hote-price', 0)

    cursor.execute("SELECT name, category, score, time, price FROM attraction WHERE priceinfomation = 'per person' AND category = %s", (selected_category,))
    rows = cursor.fetchall()

    if att_order == "price":
        # price를 기준으로 테이블 정렬
        sorted_results = sorted(rows, key=lambda x: x[4])
    elif att_order == "score":
        sorted_results = sorted(rows, key=lambda x: x[2], reverse=True)
    else:
        sorted_results = rows

    cursor.close()

    return render_template('attraction.html', categories=categories, results=sorted_results, hotel_price = hotel_price)


@bp.route('/first', methods=['POST','GET'])
def first():
    return render_template('first.html')
