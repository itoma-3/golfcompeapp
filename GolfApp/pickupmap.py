import googlemaps
import itertools
import folium
import datetime
import time
import pytz

def decode_polyline(polyline_str):
    '''デコード済みのGoogle Maps Directions APIのpolylineを返します。'''
    points = []
    index, lat, lng = 0, 0, 0

    while index < len(polyline_str):
        result, shift = 0, 0
        while True:
            b = ord(polyline_str[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lat += result & 1 and ~(result >> 1) or result >> 1

        result, shift = 0, 0
        while True:
            b = ord(polyline_str[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lng += result & 1 and ~(result >> 1) or result >> 1

        points.append((lat / 1E5, lng / 1E5))
    
    return points

def extract_points_from_route(directions_result):
    points = []
    # 経路情報が含まれる最初のルートを取得
    route = directions_result[0]
    # ルート内の各レグ（経路の一部）に対してループ
    for leg in route['legs']:
        # 各レグ内のステップ（個々の移動指示）に対してループ
        for step in leg['steps']:
            # ステップの始点の緯度と経度を取得
            start_location = step['start_location']
            points.append((start_location['lat'], start_location['lng']))
    return points
# APIキーを設定
gmaps = googlemaps.Client(key='AIzaSyARv0jbVKayU-rr1c130WRSd3sROqbyxYo')

# 出発地点、目的地、ウェイポイントの住所
start = "東京都目黒区五本木2丁目19-11"
end = "山梨県大月市大月町花咲1872-1"
waypoints = ["東京都港区白金５丁目１５−５", "東京都目黒区柿の木坂３丁目２−１８"]

# 指定した到着時刻
desired_arrival_local = datetime.datetime(2024, 4, 5, 8, 0)

# タイムゾーンを指定（例：日本標準時）
local_tz = pytz.timezone("Asia/Tokyo")

# ローカル時刻をタイムゾーン情報付きのdatetimeオブジェクトに変換
desired_arrival_local = local_tz.localize(desired_arrival_local)

# UTCエポック秒に変換
epoch_arrival = int(desired_arrival_local.timestamp())

# Directions APIを使用して経路と所要時間を計算
directions_result = gmaps.directions(start, end, mode="driving", waypoints=waypoints, optimize_waypoints=True, arrival_time=epoch_arrival, language="ja")


# 経路の詳細を表示
route = directions_result[0]  # 最初の経路を選択
legs = route['legs']  # 経路の各セグメント

# 各セグメント（Leg）の情報を表示
total_duration = 0
total_distance = 0
for leg in legs:
    print(f"出発地点: {leg['start_address']} -> 目的地: {leg['end_address']}")
    print(f"距離: {leg['distance']['text']}、所要時間: {leg['duration']['text']}")
    total_distance += leg['distance']['value']
    total_duration += leg['duration']['value']
    print("-----")

# 総距離と総所要時間を表示
print(f"総距離: {total_distance / 1000} km")
print(f"総所要時間: {total_duration / 60} 分")
# 出発時刻を計算し、表示
# 経路の詳細を取得し、総所要時間を計算
total_duration_seconds = sum(leg['duration']['value'] for leg in directions_result[0]['legs'])

# 指定した到着時刻から総所要時間を引いて、出発時刻を計算（エポック秒）
departure_time_epoch = epoch_arrival - total_duration_seconds

# エポック秒をローカルタイムゾーンのdatetimeオブジェクトに変換
departure_time_local = datetime.datetime.fromtimestamp(departure_time_epoch, tz=pytz.utc).astimezone(local_tz)

# 出発時刻を表示（ローカルタイムゾーン）
print(f"推奨出発時刻（ローカルタイムゾーン）: {departure_time_local.strftime('%Y-%m-%d %H:%M:%S')}")

# 出発時刻からスタート
current_time = departure_time_local

print(f"出発時刻（ローカルタイムゾーン）: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

for index, leg in enumerate(directions_result[0]['legs']):
    # 各レグの所要時間（秒単位）を取得
    leg_duration_seconds = leg['duration']['value']
    
    # 現在時刻に所要時間を加算して、このレグの終了時刻（次の経由地または目的地への到着時刻）を計算
    arrival_time = current_time + datetime.timedelta(seconds=leg_duration_seconds)
    
    # 到着時刻を表示
    if index < len(directions_result[0]['legs']) - 1:
        print(f"経由地 {index + 1} に到着する時刻: {arrival_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"目的地に到着する時刻: {arrival_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 現在時刻を更新
    current_time = arrival_time


# 地図を初期化（最初のレグの出発点を中心に）
start_point = directions_result[0]['legs'][0]['start_location']
map = folium.Map(location=[start_point['lat'], start_point['lng']], zoom_start=10)

# Directions APIから取得した経路（legs）を元に、地図上に経路を描画
for leg in legs:
    # 各レグのスタートとエンドのポイント
    start_loc = [leg['start_location']['lat'], leg['start_location']['lng']]
    end_loc = [leg['end_location']['lat'], leg['end_location']['lng']]
    # レグのスタート地点にマーカーを追加
    folium.Marker(start_loc, popup=leg['start_address']).add_to(map)
    # レグの経路（ポリライン）を描画
    steps = leg['steps']
    for step in steps:
        # 各ステップのpolylineをデコードして地図上に描画
        polyline = decode_polyline(step['polyline']['points'])
        folium.PolyLine(polyline, color='blue', weight=3, opacity=0.8).add_to(map)

# レグのエンド地点にマーカーを追加（最後のレグのみ）
folium.Marker(end_loc, popup=legs[-1]['end_address']).add_to(map)

# 地図をHTMLファイルとして保存
map.save('complete_route_map.html')