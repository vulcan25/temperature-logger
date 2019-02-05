import requests , json
import datetime
import random

__version__ = '0.1.0'

def conv(o):
    """ helper function used by json.dump to 
        process the datetime, without error.
    """
    if isinstance(o, datetime.datetime):
        return o.__str__()

class Report():

    def __init__(self, url, sensors, private_key):
        self.url = url
        self.sensors = sensors
        self.readings = []
        self.private_key = private_key
 
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
                                 'key': self.private_key
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
        dataset.append ({'y': random.randint(-20, 20),
                         'line_name':'TEST',
                         'x': datetime.datetime.now(),
                         'key': self.private_key })
        self.readings = dataset

    def submit(self):
        """ Pass the readings to the endpoint """

        headers = {'Content-type': 'application/json'}        
        
        try:
            r = requests.post(self.url,
                              data=json.dumps(self.readings, default=conv),
                              headers=headers)
        
            try:
                if r.status_code == 201:
                    self.readings = []
                    print ('success')
                else:
                    print('Inner fail')# pass #print (r.json())
            except:
                print('middle fail')
        except Exception as e:
            print ('outer fail')
            #iprint ('Failed to Connect.', e , r.status_code)


        
        

