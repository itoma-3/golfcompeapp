import googlemaps
import itertools
import folium


from datetime import datetime

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

# 現在地の緯度経度
my_location = (35.689487, 139.691706)  # 例：東京駅の緯度経度

# Places APIを使用して近くのゴルフ場を検索
places_result = gmaps.places_nearby(location=my_location, radius=500000, keyword='静ヒルズ')

# 結果を表示
for place in places_result['results']:
    print(f"Name: {place['name']}")
    print(f"Address: {place.get('vicinity')}")
    print(f"Location: {place['geometry']['location']}")
    print("-----")
# 出発地点、目的地、ウェイポイントの住所
start = "東京都目黒区五本木2丁目19-11"
end = "山梨県大月市大月町花咲1872-1"
waypoints = [ "東京都港区白金５丁目１５−５", "東京都目黒区柿の木坂３丁目２−１８"]

# 全てのウェイポイントの組み合わせを生成
all_combinations = []
for r in range(1, len(waypoints) + 1):
    combinations = itertools.combinations(waypoints, r)
    all_combinations.extend(combinations)

# 最適なピックアップ組み合わせを見つける
optimal_combination = None
shortest_duration = float('inf')

for combination in all_combinations:
    # ここで各組み合わせの経路と所要時間を計算します（省略）
    # 疑似コード: duration = calculate_route_duration(start, end, combination)
    duration = 0  # 仮の値
    
    if duration < shortest_duration:
        shortest_duration = duration
        optimal_combination = combination

# 結果を表示
print(f"最適なピックアップ組み合わせ: {optimal_combination}")

# Directions APIを使用して経路を取得
directions_result = gmaps.directions(start, end, departure_time=datetime.now())

# 経路上のポイントを抽出（ここでは疑似コードとして簡略化）
points_on_route = extract_points_from_route(directions_result)

# 経路上の駅を格納するリスト
stations_on_route = []

# 各ポイント周辺の鉄道駅を検索
for point in points_on_route:
    # Places APIを使用して鉄道駅を検索（ここでは疑似コード）
    places_result = gmaps.places_nearby(location=point, radius=500, type='train_station', language='ja')
    
    # 検索結果から駅の情報を抽出してリストに追加
    for place in places_result['results']:
        station_info = {
            'name': place['name'],
            'location': place['geometry']['location']
        }
        if station_info not in stations_on_route:
            stations_on_route.append(station_info)

# 重複を除去した駅の情報を表示
for station in stations_on_route:
    print(f"駅名: {station['name']}, 位置: {station['location']}")

