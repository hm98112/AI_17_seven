from flask import Blueprint, render_template, request, current_app
import psycopg2

bp = Blueprint('index', __name__, url_prefix='/')


#연결 설정
conn = psycopg2.connect(
    database="ai-17-seven",
    user="hm98112",
    password="123456!@#",
    host="34.64.57.43",
    port="5432"
)




#"/attraction" url 접근 함수
@bp.route('/attraction', methods=['POST', 'GET'])
def index():

    #전역 변수에 이전 페이지(호텔)에서 넘어온 가격 저장
    current_app.config['hotel_price'] = request.form.get('hotel-price')
    current_app.config['hotelTotalPrice'] = request.form.get('hotelTotalPrice')
    current_app.config['count_people'] = request.form.get('count_people')

    cursor = conn.cursor()
    #카테고리 리스트
    cursor.execute("SELECT DISTINCT category FROM attraction")
    categories = cursor.fetchall()
    
    #어트랙션 초기 테이블 출력(10개에서 자름)
    cursor.execute("SELECT name, category, score, time, price FROM attraction")
    rows = cursor.fetchmany(10)
    cursor.close()
    
    return render_template('attraction.html', 
                           categories=categories, 
                           results = rows[:10], 
                           count_people = current_app.config['count_people']
                           )

#"/attraction/price-selection" url 접근 함수 |어트랙션 가격 확인 기능 동작|
@bp.route('/attraction/price-selection', methods=['POST','GET'])
def price_selection():
    
    # POST 메소드로 전송된 데이터를 request 객체를 통해 액세스 가능
    count_people = current_app.config['count_people']
    
    #필터에서 선택한 특성들 불러오기
    selected_category = request.form.get('attraction-category')
    att_order = request.form.get('order')
    cursor = conn.cursor()

    #선택 리스트 요소 저장
    cursor.execute("SELECT DISTINCT category FROM attraction")
    categories = cursor.fetchall()

    #필터링 쿼리 처리
    cursor.execute("SELECT name, category, score, time, price FROM attraction WHERE priceinfomation = 'per person' AND category = %s", (selected_category,))
    rows = cursor.fetchall()

    if att_order == "price":
        # price를 기준으로 테이블 정렬
        sorted_results = sorted(rows, key=lambda x: x[4])
    elif att_order == "score":
        # score 기준으로 테이블 정렬
        sorted_results = sorted(rows, key=lambda x: x[2], reverse=True)
    else:
        sorted_results = rows

    cursor.close()

    return render_template('attraction.html', categories=categories,count_people=count_people, results=sorted_results, att_order=att_order,selected_category=selected_category)



