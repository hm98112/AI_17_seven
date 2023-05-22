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



@bp.route('/attraction')
def index():
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT category FROM attraction")
    categories = cursor.fetchall()
    
    cursor.execute("SELECT name, category, score, time, price FROM attraction")
    rows = cursor.fetchall()
    
    cursor.close()

    return render_template('attraction.html', categories=categories, results = rows)

@bp.route('price-selection', methods=['POST'])
def price_selection():
    selected_category = request.form.get('attraction-category')
    att_order = request.form.get('order')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT category FROM attraction")
    categories = cursor.fetchall()

    
    cursor.execute("SELECT name, category, score, time, price FROM attraction WHERE category = %s", (selected_category,))
    rows = cursor.fetchall()

    if att_order == "price":
        # price를 기준으로 테이블 정렬
        sorted_results = sorted(rows, key=lambda x: x[4])
    elif att_order == "score":
        sorted_results = sorted(rows, key=lambda x: x[2], reverse=True)
    else:
        sorted_results = rows

    cursor.close()

    return render_template('attraction.html', categories=categories, results=sorted_results)
