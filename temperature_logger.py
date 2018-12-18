import requests , json
import datetime

__version__ = '0.1.0'

def conv(o):
    """ helper function used by json.dump to 
        process the datetime, without error.
    """
    if isinstance(o, datetime.datetime):
        return o.__str__()

class Report():

    def __init__(self, url, sensors):
        self.url = url
        self.sensors = sensors
        self.readings = []
 
    def read_temps(self):
        """ Read the temperature from each sensor """
        try:
            import temperature
            dataset = self.readings
            
            date = datetime.datetime.now()
            
            # Get the actual temperature reading
            for sensor in self.sensors:
                dataset.append ({'line_name':sensor,
                                 'x': date,
                                 'y':temperature.read_temp(sensor),
                                 'key': 'PRIV'
                                  })
            # Update the readings
            self.readings = dataset
        except:
            # `import temp` has probably failed, load test temperatures
            # This should only execute when not on a Pi.

            print('Reverting to test mode')
            self.test_read_temps()

    def test_read_temps(self):
        dataset = self.readings
        dataset.append ({'y': 8,
                         'line_name':'TEST',
                         'x': datetime.datetime.now(),
                         'key': 'PRIV' })
        self.readings = dataset

    def submit(self):
        """ Pass the readings to the endpoint """

        headers = {'Content-type': 'application/json'}        
        
        try:
            print('Server Response: ', requests.post(self.url,
                               data=json.dumps(self.readings, default=conv),
                               headers=headers ).text)
            # reset the readings, as all have been submitted.
            self.readings = []
        except requests.exceptions.ConnectionError as e:
            print ('Failed to Connect.')

