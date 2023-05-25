from flask import Blueprint, render_template, request
import psycopg2

bp = Blueprint('airline', __name__, url_prefix='/')


conn = psycopg2.connect(
    database="ai-17-seven",
    user="khs03",
    password="1234!",
    host="34.64.57.43",
    port="5432"
)

#가격 확인을 위한 선택리스트 요소 추출 함수
def air_select_list():
    cursor = conn.cursor()

    #날짜 리스트
    cursor.execute("SELECT DISTINCT date FROM parair")
    departure_dates = cursor.fetchall()

    cursor.execute("SELECT DISTINCT date FROM corair")
    return_dates = cursor.fetchall()

    #좌석 리스트
    cursor.execute("SELECT DISTINCT seat FROM parair")
    departure_seats = cursor.fetchall()

    cursor.execute("SELECT DISTINCT seat FROM corair")
    return_seats = cursor.fetchall()
    cursor.close()  

    return departure_dates, departure_seats, return_dates, return_seats

#"/airline" url 접근 함수
@bp.route('/airline', methods=['POST','GET'])
def index():
    cursor = conn.cursor()
    
    selected_departure_date = request.form.get('departure-date')
    selected_return_date = request.form.get('return-date')
    selected_departure_seat = request.form.get('departure-seat')
    selected_return_seat = request.form.get('return-seat')
    att_order = request.form.get('order')
    #선택 리스트 요소 저장
    departure_dates, departure_seats, return_dates, return_seats = air_select_list()


    #항공권 초기 테이블 출력(10개에서 자름)
    cursor.execute("SELECT date, airline, dep, arr, deptime, arrtime, seat, time, day, price FROM parair")
    rows = cursor.fetchmany(10)

    cursor.execute("SELECT date, airline, dep, arr, deptime, arrtime, seat, time, day, price FROM corair")
    return_rows = cursor.fetchmany(10)
    cursor.close()  

    return render_template('airline.html', 
                           departure_dates=departure_dates, departure_seats=departure_seats, 
                           return_dates=return_dates, return_seats=return_seats, 
                           results=rows, return_results=return_rows,
                           selected_departure_date = selected_departure_date, selected_return_date = selected_return_date,
                           selected_departure_seat = selected_departure_seat, selected_return_seat = selected_return_seat,
                           att_order = att_order                           
                           )

#"/airline/price-selection" url 접근 함수 |항공권 가격 확인 기능 동작|
@bp.route('/airline/price-selection', methods=['POST'])
def price_selection():
    
    #필터에서 선택한 특성들 불러오기
    selected_departure_date = request.form.get('departure-date')
    selected_return_date = request.form.get('return-date')
    selected_departure_seat = request.form.get('departure-seat')
    selected_return_seat = request.form.get('return-seat')
    att_order = request.form.get('order')
    print(att_order)
    
    cursor = conn.cursor()

    #선택 리스트 요소 저장
    departure_dates, departure_seats, return_dates, return_seats = air_select_list()


    #필터링 쿼리 처리
    cursor.execute("SELECT date, airline, dep, arr, deptime, arrtime, seat, time, day, price FROM parair WHERE date = %s AND seat = %s", (selected_departure_date, selected_departure_seat))
    rows = cursor.fetchall()

    if att_order == "price":
        sorted_results = sorted(rows, key=lambda x: x[9])
    elif att_order == "airline":
        sorted_results = sorted(rows, key=lambda x: x[1], reverse=True)
    else:
        sorted_results = rows

    cursor.execute("SELECT date, airline, dep, arr, deptime, arrtime, seat, time, day, price FROM corair WHERE date = %s AND seat = %s", (selected_return_date, selected_return_seat))
    return_rows = cursor.fetchall()

    if att_order == "price":
        sorted_return_results = sorted(return_rows, key=lambda x: x[9])
    elif att_order == "airline":
        sorted_return_results = sorted(return_rows, key=lambda x: x[1], reverse=True)
    else:
        sorted_return_results = return_rows

    cursor.close()

    return render_template('airline.html', 
                           departure_dates=departure_dates, departure_seats=departure_seats, 
                           return_dates=return_dates, return_seats=return_seats, 
                           results=sorted_results, return_results=sorted_return_results,
                           selected_departure_date = selected_departure_date, selected_return_date = selected_return_date,
                           selected_departure_seat = selected_departure_seat, selected_return_seat = selected_return_seat,
                           att_order= att_order
                           )

