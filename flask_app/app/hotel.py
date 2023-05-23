from flask import Blueprint, render_template, request
import psycopg2

bp = Blueprint('hotel', __name__, url_prefix='/')



conn = psycopg2.connect(
    database="ai-17-seven",
    user="hm98112",
    password="123456!@#",
    host="34.64.57.43",
    port="5432"
)



@bp.route('/hotel', methods=['POST', 'GET'])
def index():

    air_price = request.form.get('air-price', 0)

    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT grade FROM hotel678")
    grade = sorted(cursor.fetchall())

    cursor.execute("SELECT DISTINCT checkin FROM hotel678")
    checkin = sorted(cursor.fetchall())

    cursor.execute("SELECT DISTINCT evaluation FROM hotel678")
    evaluation = sorted(cursor.fetchall())
    evaluation.pop(4)
    evaluation.pop()
    
    cursor.execute("SELECT name, grade, score, evaluation, price, disprice, service, checkin FROM hotel678")
    rows = cursor.fetchall()[:20]
    
    cursor.close()

    return render_template('hotel.html', grades=grade, checkins = checkin, evaluations = evaluation, results = rows[:10], air_price=air_price)

@bp.route('/hotel/price-selection', methods=['POST'])
def price_selection():
    air_price = request.form.get('air-price', 0)


    selected_checkin = request.form.get('hotel-checkins')
    selected_grade = request.form.get('hotel-grade')
    selected_evaluation = request.form.get('hotel-evaluation')
    hotel_order = request.form.get('order')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT grade FROM hotel678")
    grade = sorted(cursor.fetchall())

    cursor.execute("SELECT DISTINCT checkin FROM hotel678")
    checkin = sorted(cursor.fetchall())

    cursor.execute("SELECT DISTINCT evaluation FROM hotel678")
    evaluation = sorted(cursor.fetchall())
    evaluation.pop(4)
    evaluation.pop()
    

    cursor.execute(f"SELECT name, grade, score, evaluation, price, disprice, service, checkin FROM hotel678 WHERE checkin = '{selected_checkin}' AND grade = {selected_grade} AND evaluation ='{selected_evaluation.lstrip().rstrip()} '")
    rows = cursor.fetchall()

    if hotel_order == "price":
        # price를 기준으로 테이블 정렬
        sorted_results = sorted(rows, key=lambda x: x[4])
    elif hotel_order == "score":
        sorted_results = sorted(rows, key=lambda x: x[2], reverse=True)
    else:
        sorted_results = rows

    cursor.close()

    return render_template('hotel.html', grades=grade, checkins = checkin, evaluations = evaluation, results = sorted_results, air_price=air_price)



