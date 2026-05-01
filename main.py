import json, unittest, datetime

# --- Replace file reading with direct data ---

jsonData1 = {
    "deviceID": "dh28dslkja",
    "deviceType": "LaserCutter",
    "timestamp": 1624445837783,
    "location": "japan/tokyo/keiyō-industrial-zone/daikibo-factory-meiyo/section-1",
    "operationStatus": "healthy",
    "temp": 22
}

jsonData2 = {
    "device": {
        "id": "dh28dslkja",
        "type": "LaserCutter"
    },
    "timestamp": "2021-06-23T10:57:17.783Z",
    "country": "japan",
    "city": "tokyo",
    "area": "keiyō-industrial-zone",
    "factory": "daikibo-factory-meiyo",
    "section": "section-1",
    "data": {
        "status": "healthy",
        "temperature": 22
    }
}

jsonExpectedResult = {
    "deviceID": "dh28dslkja",
    "deviceType": "LaserCutter",
    "timestamp": 1624445837783,
    "location": {
        "country": "japan",
        "city": "tokyo",
        "area": "keiyō-industrial-zone",
        "factory": "daikibo-factory-meiyo",
        "section": "section-1"
    },
    "data": {
        "status": "healthy",
        "temperature": 22
    }
}

# --- Conversion functions ---

def convertFromFormat1(jsonObject):
    locationParts = jsonObject["location"].split("/")

    return {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }

def convertFromFormat2(jsonObject):
    dt = datetime.datetime.fromisoformat(jsonObject['timestamp'].replace("Z", "+00:00"))
    timestamp = int(dt.timestamp() * 1000)

    return {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': jsonObject['data']
    }

def main(jsonObject):
    if jsonObject.get('device') is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)

# --- Tests ---

class TestSolution(unittest.TestCase):

    def test_dataType1(self):
        self.assertEqual(main(jsonData1), jsonExpectedResult)

    def test_dataType2(self):
        self.assertEqual(main(jsonData2), jsonExpectedResult)

if __name__ == '__main__':
    unittest.main()
