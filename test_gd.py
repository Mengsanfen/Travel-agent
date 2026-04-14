import requests
import webbrowser
from pathlib import Path

# ========== 配置 ==========
AMAP_WEB_KEY = "c268c02a6060b5113dc3eafe7676a9d5"
AMAP_JS_KEY = "a107b3f8e34d3d6d468e945cfb05c214"
PLACE_NAME = "成都天府广场"

# ========== 1. 调用高德地理编码 API（Web服务） ==========
url = "https://restapi.amap.com/v3/geocode/geo"
params = {
    "key": AMAP_WEB_KEY,
    "address": PLACE_NAME
}

resp = requests.get(url, params=params, timeout=10)
data = resp.json()

if data.get("status") != "1":
    raise RuntimeError(f"高德 API 调用失败: {data}")

location = data["geocodes"][0]["location"]
lng, lat = location.split(",")

print(f"📍 {PLACE_NAME} 经纬度：{lng}, {lat}")

# ========== 2. 生成 HTML 地图（JS API） ==========
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>高德地图示例</title>
    <style>
        html, body, #container {{
            width: 100%;
            height: 100%;
            margin: 0;
        }}
    </style>
    <script src="https://webapi.amap.com/maps?v=2.0&key={AMAP_JS_KEY}"></script>
</head>
<body>
<div id="container"></div>

<script>
    var map = new AMap.Map('container', {{
        zoom: 15,
        center: [{lng}, {lat}]
    }});

    var marker = new AMap.Marker({{
        position: [{lng}, {lat}],
        title: "{PLACE_NAME}"
    }});

    map.add(marker);
</script>
</body>
</html>
"""

html_path = Path("map.html")
html_path.write_text(html_content, encoding="utf-8")

webbrowser.open(html_path.absolute().as_uri())
print("✅ 地图已在浏览器中打开")
