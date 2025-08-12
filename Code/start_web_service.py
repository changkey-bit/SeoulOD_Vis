from flask import Flask, render_template, request
import os
import pandas as pd
import csv
from time import time
from datetime import datetime
from show_map import Showmap

# 파일 경로 및 환경 설정
# NOTE: 이 경로는 실제 파일 위치에 맞게 수정해야 합니다.
BASE_DIR = os.getcwd()
DATA_DIR = '../Data'
POLY_PATH = '../PolyCode/inseoul_polycode.pkl'
ORIGIN_PATH = '../PolyCode/kt_origin_code.pkl'
DEST_PATH = '../PolyCode/kt_destination_code.pkl'

'''
https://wooiljeong.github.io/python/mapboxgl/
위의 링크 참고해서 아래 TOKEN에 본인 토큰 넣기
'''

# Mapbox API 토큰
TOKEN = "TOKEN_HERE"  # 여기에 본인의 Mapbox 토큰을 입력하세요
LOG_CSV = DATA_DIR + '/LogData/loading_test.csv'

# 애플리케이션 시작 시 한 번만 정적 데이터 로드
try:
    polydata = pd.read_pickle(POLY_PATH)
    origin_data = pd.read_pickle(ORIGIN_PATH)
    des_data = pd.read_pickle(DEST_PATH)
except FileNotFoundError as e:
    print(f"Error: Could not load pickle files. Check your paths. {e}")
    polydata, origin_data, des_data = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Flask 앱 및 Showmap 클래스 초기화
app = Flask(__name__)
showmap = Showmap(DATA_DIR, origin_data, des_data, polydata, TOKEN)


# 유틸리티 함수: 로그 기록
def log_loading(route: str, duration: float):
    """
    지도 생성에 걸린 시간을 CSV 파일에 기록합니다.
    """
    t_date = datetime.now().strftime('%Y.%m.%d - %H:%M:%S')
    with open(LOG_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([t_date, f"{duration:.2f}", route])


@app.route('/')
def first():
    """
    초기 페이지를 렌더링합니다.
    """
    return render_template('first_page.html')


@app.route('/main')
def main():
    """
    메인 페이지를 렌더링하고, 초기 지도 HTML을 포함합니다.
    """
    try:
        with open('templates/new_init_map.html', encoding='utf-8') as f:
            init_map = f.read()
    except FileNotFoundError:
        init_map = '<p>Initial map template not found.</p>'
    return render_template('index.html', map_html=init_map)


@app.route('/main/heat', methods=['POST'])
def heat():
    """
    히트맵 요청을 처리하고, Pydeck 지도를 생성하여 반환합니다.
    """
    start = time()

    sex_input = request.form['sex']
    if sex_input == '남성+여성':
        gender_param = ['남성', '여성']
    else:
        gender_param = [sex_input]

    # 폼 데이터 추출
    params = {
        'year': request.form.getlist('year'),
        'month': [request.form['month']],
        'hour': request.form.getlist('hour'),
        'age': request.form.getlist('age'),
        'move': request.form['od'],
        'gender': gender_param,
        'metric': request.form['distribution'],
        'palette': request.form['map_color'],  # 변수 이름 통일
        'maxscale': request.form.get('criteria_value', '선택안함'),
        'focus_poly': request.form.get('numberInput1', None)
    }

    # Showmap 클래스의 heatmap 메서드 호출
    html = showmap.heatmap(**params)
    duration = time() - start
    log_loading('heat', duration)

    # 렌더링 시 선택된 값 유지
    return render_template('index.html', map_html=html,
                           selected_year1=params['year'], selected_month1=params['month'][0],
                           selected_hour1=params['hour'], selected_age1=params['age'],
                           selected_od1=params['move'], selected_sex1=params['gender'],
                           selected_dist1=params['metric'], selected_color1=params['palette'],
                           selected_criteria1=params['maxscale'], selected_button='heat',
                           input_poly_heat=params['focus_poly'] or '')


@app.route('/main/flow', methods=['POST'])
def flow():
    """
    플로우맵 요청을 처리하고, Pydeck 지도를 생성하여 반환합니다.
    """
    start = time()

    sex_input = request.form['sex']
    if sex_input == '남성+여성':
        gender_param = ['남성', '여성']
    else:
        gender_param = [sex_input]

    # 폼 데이터 추출
    params = {
        'year': request.form.getlist('year'),
        'month': [request.form['month']],
        'hour': request.form.getlist('hour'),
        'age': request.form.getlist('age'),
        'gender': gender_param,
        'metric': request.form['distribution'],
        'palette': request.form['map_color'],  # 변수 이름 통일
        'minscale': request.form.get('criteria_value', '선택안함'),
        'origin': request.form.get('numberInput2', None),
        'destination': request.form.get('numberInput3', None)
    }

    # Showmap 클래스의 flowmap 메서드 호출
    html = showmap.flowmap(**params)
    duration = time() - start
    log_loading('flow', duration)

    # 렌더링 시 선택된 값 유지
    return render_template('index.html', map_html=html,
                           selected_year2=params['year'], selected_month2=params['month'][0],
                           selected_hour2=params['hour'], selected_age2=params['age'],
                           selected_sex2=params['gender'], selected_dist2=params['metric'],
                           selected_color2=params['palette'], selected_criteria2=params['minscale'],
                           selected_button='flow', input_poly_flow1=params['origin'] or '',
                           input_poly_flow2=params['destination'] or '')


if __name__ == '__main__':
    app.run(debug=True)

