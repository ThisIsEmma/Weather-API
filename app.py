import os
import time
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL ='https://api.openweathermap.org/data/2.5/weather?q={q}&appid={appid}'


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/results', methods=['GET'])
def results():
    """Displays results for current weather conditions."""
    # TODO: Use 'request.args' to retrieve the city & units from the query
    # parameters.
    city_name = request.args.get('city')
    units = request.args.get('units')

    # TODO: Enter query parameters here for the 'appid' (your api key),
    # the city, and the units (metric or imperial).
    # See the documentation here: https://openweathermap.org/current

    result_json = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}', params = {'units': units}).json()
    
    # Uncomment the line below to see the results of the API call!
    # pp.pprint(result_json)

    # TODO: Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.
    context = {
        'date': datetime.now(),
        'city': result_json['name'],
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunset' : datetime.fromtimestamp((result_json['sys']['sunset'])),
        'sunrise' : datetime.fromtimestamp((result_json['sys']['sunrise'])),
        'units_letter': get_letter_for_units(units),
        'icon': result_json['weather'][0]['icon'],
    }

    return render_template('results.html', **context)

# Helper function for the ('/comparison_results') route:
def get_city_data(city, units):

    result_json = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}', params = {'units': units}).json()
    city_data = {
        'date': datetime.now(),
        'name': result_json['name'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunset': datetime.fromtimestamp((result_json['sys']['sunset'])),
        'units_letter': get_letter_for_units(units)
    }

    return city_data

@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    print('comparison results route!')
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('units')
   

    # TODO: Make 2 API calls, one for each city. HINT: You may want to write a 
    # helper function for this!
    city1_data = get_city_data(city1, units)
    city2_data = get_city_data(city2, units)

    # TODO: Pass the information for both cities in the context. Make sure to
    # pass info for the temperature, humidity, wind speed, and sunset time!
    # HINT: It may be useful to create 2 new dictionaries, `city1_info` and 
    # `city2_info`, to organize the data.
    context = {
        'city1' : city1_data,
        'city2' : city2_data,
        'units' : get_letter_for_units(units)
    }

    return render_template('comparison_results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
