import gc
from glob import glob
import pandas as pd
import pydeck as pdk

# pydeck.colors.color_scales가 더 이상 지원되지 않으므로, 수동으로 팔레트를 정의합니다.
COLOR_SCALES = {
    'PURP': [
        [247, 244, 249], [231, 225, 239], [212, 185, 218],
        [201, 148, 199], [178, 107, 181], [146, 52, 159],
        [112, 29, 137], [84, 1, 104]
    ],
    # 필요에 따라 다른 색상 팔레트를 추가할 수 있습니다.
    'GREENS': [
        [237, 248, 233], [199, 233, 192], [161, 217, 155],
        [116, 196, 118], [65, 171, 93], [35, 139, 69],
        [0, 109, 44], [0, 68, 27]
    ]
}


def normalize_list(values, maxscale=None):
    """
    주어진 값 리스트를 0과 1 사이로 정규화합니다.
    """
    series = pd.Series(values, dtype=float)
    if maxscale and maxscale != '선택안함':
        # 최대값(maxscale)을 기준으로 정규화
        norm = (series / float(maxscale)).clip(0, 1)
    else:
        # 데이터의 최소/최대값을 기준으로 정규화
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return [0.0] * len(series)
        norm = (series - min_val) / (max_val - min_val)
    return norm.tolist()


class Showmap:
    """
    데이터를 필터링하고 Pydeck을 사용해 히트맵 및 플로우맵을 생성하는 클래스입니다.
    """

    def __init__(self, data_dir, origin_df, dest_df, poly_df, token):
        """
        클래스 초기화 시 필요한 데이터와 API 토큰을 설정합니다.
        """
        self.data_dir = data_dir
        self.origin_df = origin_df
        self.dest_df = dest_df
        self.poly_df = poly_df.astype({'polycode': 'uint32'})
        pdk.settings.mapbox_api_key = token

    def _filter_and_load(self, subfolder, filters):
        """
        주어진 필터를 기반으로 데이터를 로드합니다.
        """
        path = f"{self.data_dir}/{subfolder}/*.pkl"
        files = glob(path)

        for key, sel in filters.items():
            if not sel or sel == '선택안함' or sel == ['선택안함']:
                continue

            if isinstance(sel, (list, tuple)):
                files = [f for f in files if any(s in f for s in sel)]
            else:
                files = [f for f in files if sel in f]

        dfs = []
        for f in files:
            try:
                dfs.append(pd.read_pickle(f))
            except Exception as e:
                print(f"Error loading {f}: {e}")
                continue

        df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        gc.collect()
        return df

    def _prepare_polygons(self, metrics_df, metric_col, maxscale, palette):
        """
        지표 데이터와 폴리곤 데이터를 병합하고 색상을 계산합니다.
        """
        merged = self.poly_df.merge(metrics_df, on='polycode').dropna().reset_index(drop=True)
        norm_vals = normalize_list(merged[metric_col], maxscale)

        # 정의된 COLOR_SCALES에서 팔레트 선택
        color_scale = COLOR_SCALES.get(palette.upper(), COLOR_SCALES['PURP'])

        if norm_vals:
            merged['fill_color'] = [color_scale[int(v * (len(color_scale) - 1))] for v in norm_vals]
        else:
            merged['fill_color'] = [[200, 200, 200]] * len(merged)
        return merged

    def heatmap(self, year, month, hour, age, move, gender, metric, palette, maxscale='선택안함', focus_poly=None):
        """
        히트맵을 생성하고 HTML 문자열로 반환합니다.
        """
        # 데이터 필터링 및 로드
        filters = {'year': year, 'month': month, 'hour': hour, 'age': age, 'move': move, 'gender': gender}
        df = self._filter_and_load('heat', filters)
        if df.empty:
            return '<p>데이터가 없습니다.</p>'

        # 데이터 집계
        grouped = df.groupby('polycode').agg(
            ttime=('ttime', 'mean'),
            dist=('dist', 'mean'),
            personcount=('personcount', 'sum')
        ).reset_index()

        # 폴리곤에 지표 병합 및 색상 계산. 수정된 _prepare_polygons 사용.
        colored = self._prepare_polygons(grouped, metric, maxscale, palette)

        # 지도 중심 설정
        center = [126.986, 37.565]
        zoom = 10
        if focus_poly:
            try:
                row = self.origin_df.query(f'origin=={int(focus_poly)}')
                if not row.empty:
                    center = [row.lon_ori.iloc[0], row.lat_ori.iloc[0]]
                    zoom = 14
            except (ValueError, IndexError):
                pass

        # Pydeck 레이어 및 덱 생성
        base = pdk.Layer(
            'PolygonLayer', self.poly_df, get_polygon='coordinates', get_fill_color='[200, 200, 200]',
            pickable=False, stroked=True, opacity=0.3
        )
        layer = pdk.Layer(
            'PolygonLayer', colored, get_polygon='coordinates', get_fill_color='fill_color',
            pickable=True, stroked=True, opacity=0.8,
            tooltip={"html": "<b>{polycode}</b><br>총 인원: {personcount}명, 평균 거리: {dist:.2f}m, 평균 시간: {ttime:.2f}분"}
        )
        deck = pdk.Deck(
            layers=[base, layer],
            initial_view_state=pdk.ViewState(longitude=center[0], latitude=center[1], zoom=zoom),
        )
        return deck.to_html(as_string=True, notebook_display=False)

    def flowmap(self, year, month, hour, age, gender, metric, palette, minscale='선택안함', origin=None, destination=None):
        """
        플로우맵을 생성하고 HTML 문자열로 반환합니다.
        """
        # 데이터 로드
        filters = {'year': year, 'month': month, 'hour': hour, 'age': age, 'gender': gender}
        df = self._filter_and_load('flow', filters)
        if df.empty:
            return '<p>데이터가 없습니다.</p>'

        # 출발지/도착지 필터링
        if origin: df = df[df.origin == int(origin)]
        if destination: df = df[df.destination == int(destination)]
        df = df[df.origin != df.destination]

        # 데이터 집계
        agg = df.groupby(['origin', 'destination']).agg(
            personcount=('personcount', 'sum'),
            dist=('dist', 'mean'),
            ttime=('ttime', 'mean')
        ).reset_index()

        agg['versus_time'] = (agg.ttime / agg.dist).round(2)

        if minscale != '선택안함':
            agg = agg[agg[metric] >= float(minscale)]

        # 좌표 데이터 병합
        agg = agg.merge(self.origin_df, on='origin').merge(self.dest_df, on='destination')

        # 너비 정규화
        agg['minmax'] = normalize_list(agg[metric])

        # 지도 중심 설정
        center = [126.986, 37.565]
        zoom = 10
        if origin or destination:
            try:
                query_col = 'origin' if origin else 'destination'
                query_val = origin if origin else destination
                row = self.origin_df.query(f'{query_col}=={int(query_val)}')
                if not row.empty:
                    center = [row.lon_ori.iloc[0], row.lat_ori.iloc[0]]
                    zoom = 16
            except (ValueError, IndexError):
                pass

        # Pydeck 레이어 및 덱 생성
        base = pdk.Layer(
            'PolygonLayer', self.poly_df, get_polygon='coordinates', get_fill_color='[200, 200, 200]',
            pickable=False, stroked=True, opacity=0.3
        )
        arc = pdk.Layer(
            'ArcLayer', agg, get_source_position='[lon_ori, lat_ori]', get_target_position='[lon_des, lat_des]',
            get_width='minmax * 30', pickable=True,
            tooltip={
                "html": "<b>{origin_name}→{destination_name}</b><br>총 인원: {personcount}명, 평균 거리: {dist:.2f}m, 평균 시간: {ttime:.2f}분"}
        )
        deck = pdk.Deck(
            layers=[base, arc],
            initial_view_state=pdk.ViewState(longitude=center[0], latitude=center[1], zoom=zoom, bearing=-10, pitch=30)
        )
        return deck.to_html(as_string=True, notebook_display=False)
