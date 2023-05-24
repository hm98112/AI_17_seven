from flask import Blueprint, render_template, request, current_app
import psycopg2


bp = Blueprint('hotel', __name__, url_prefix='/')



conn = psycopg2.connect(
    database="ai-17-seven",
    user="hm98112",
    password="123456!@#",
    host="34.64.57.43",
    port="5432"
)


#가격 확인을 위한 선택리스트 요소 추출 함수
def hot_select_list():
    cursor = conn.cursor()

    #등급 리스트
    cursor.execute("SELECT DISTINCT grade FROM hotel678")
    grade = sorted(cursor.fetchall())

    #날짜 리스트
    cursor.execute("SELECT DISTINCT checkin FROM hotel678")
    checkin = sorted(cursor.fetchall())

    cursor.close()  

    return grade, checkin

#"/hotel" url 접근 함수
@bp.route('/hotel', methods=['POST', 'GET'])
def index():
    
    #전역 변수에 이전 페이지(항공권)에서 넘어온 가격, 인원 저장
    current_app.config['air_price'] = request.form.get('air-price')
    current_app.config['count_people'] = request.form.get('count_people')
    
    
    cursor = conn.cursor()

    #선택 리스트 요소 저장
    grade, checkin = hot_select_list()
    
    #호텔 초기 테이블 출력(10개에서 자름)
    cursor.execute("SELECT name, grade, score, evaluation, price, disprice, service, checkin FROM hotel678")
    rows = cursor.fetchmany(10)
    cursor.close()

    return render_template('hotel.html', grades=grade, checkins = checkin, results = rows, count_people = current_app.config['count_people'])

#"/hotel/price-selection" url 접근 함수 |호텔 가격 확인 기능 동작|
@bp.route('/hotel/price-selection', methods=['POST'])
def price_selection():
    
    #필터에서 선택한 특성들 불러오기
    selected_checkin = request.form.get('hotel-checkins')
    selected_checkout = request.form.get('hotel-checkouts')
    lb_days = request.form.get('lb_days')
    selected_grade = request.form.get('hotel-grade')
    hotel_order = request.form.get('order')
    count_people = request.form.get('count_people')
    cursor = conn.cursor()

    #선택 리스트 요소 저장
    grade, checkin = hot_select_list()
    
    #필터링 쿼리 처리
    cursor.execute(f"SELECT name, grade, score, evaluation, price, disprice, service, checkin FROM hotel678 WHERE checkin = '{selected_checkin}' AND grade = {selected_grade}")
    rows = cursor.fetchall()

    if hotel_order == "price":
        # price를 기준으로 테이블 정렬
        sorted_results = sorted(rows, key=lambda x: x[4])
    elif hotel_order == "score":
        # score 기준으로 테이블 정렬
        sorted_results = sorted(rows, key=lambda x: x[2], reverse=True)
    elif hotel_order == "evaluation":
        sorted_results = sorted(rows, key=lambda x: x[3])
    else:
        sorted_results = rows
    if selected_grade is not None:
        selected_grade = int(selected_grade)
    return render_template('hotel.html', 
                           grades=grade, 
                           lb_days = lb_days,
                           selected_checkin = selected_checkin,
                           selected_checkout = selected_checkout,
                           checkins = checkin, 
                           selected_grade = selected_grade,
                           results = sorted_results,
                           hotel_order = hotel_order,
                           count_people = count_people
                           )



