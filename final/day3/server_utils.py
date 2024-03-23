import requests as r

# получение данных с сервера
def get_target_building(data):
  colors = data.keys()
  TOKEN = "13f6dc51-55b9-40ed-b671-37ca6583bddf"
  URL = 'http://65.108.156.108/buildings'
  # массив с данными распознанных зданий
  data = [{
      "coords": data[i][0],
      "target_height": data[i][2],
      "real_height": data[i][1],
      "match": data[i][3]
    } for i in colors]
  print(data)

  headers = {"Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {TOKEN}"}

  response = r.post(URL, json=data, headers=headers)

  print("Status Code", response.status_code)
  print("JSON Response ", response.json())
  return response.json()['coords']