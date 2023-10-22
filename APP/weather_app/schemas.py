CURRENT_WEATHER_SCHEMA = {
  'type': 'object',
  'properties': {
    'name': { 'type': 'string' },
    'sys': {
      'type': 'object',
      'properties': {
        'country': { 'type': 'string' },
        'sunrise': { 'type': 'integer' },
        'sunset': { 'type': 'integer' }
      },
      'required': ['country', 'sunrise', 'sunset'],
    },
    'weather': {
      'type': 'array',
      'items': {
        'type': 'object',
        'properties': {
          'icon': { 'type': 'string' },
          'description': { 'type': 'string' }
        },
        'required': ['icon', 'description'],
      }
    },
    'main': {
      'type': 'object',
      'properties': {
        'temp': { 'type': 'number' },
        'temp_max': { 'type': 'number' },
        'temp_min': { 'type': 'number' },
        'humidity': { 'type': 'integer' }
      },
      'required': ['temp', 'temp_max', 'temp_min', 'humidity'],
    },
    'wind': {
      'type': 'object',
      'properties': {
        'speed': { 'type': 'number' }
      },
      'required': ['speed'],
    },
    'coord': {
      'type': 'object',
      'properties': {
        'lat': { 'type': 'number' },
        'lon': { 'type': 'number' }
      },
      'required': ['lat', 'lon']
    },
  },
  'required': ['name', 'sys', 'weather', 'main', 'wind', 'coord'],
}

DAILY_FORECAST_SCHEMA = {
  "type": "object",
  "properties": {
    "daily": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "dt": { "type": "integer" },
          "weather": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "icon": { "type": "string" }
              },
              "required": ["icon"]
            }
          },
          "temp": {
            "type": "object",
            "properties": {
              "min": { "type": "number" },
              "max": { "type": "number" }
            },
            "required": ["min", "max"]
          },
          "wind_speed": { "type": "number" },
          "humidity": { "type": "integer" }
        },
        "required": ["dt", "weather", "temp", "wind_speed", "humidity"]
      }
    }
  },
  "required": ["daily"]
}
