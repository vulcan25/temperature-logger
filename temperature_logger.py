import requests , json
import datetime
import random
import redis

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
        self.redis = redis.Redis(host='192.168.2.103', db=0)
 
    def read_temps(self):
        """ Read the temperature from each sensor """
        try:
            import temperature
            dataset = self.readings
            
            date = datetime.datetime.now()
            
            # Get the actual temperature reading
            for sensor in self.sensors:
                the_temp = temperature.read_temp(sensor)
                dataset.append ({'line_name':sensor,
                                 'x': date,
                                 'y':the_temp,
                                 'key': self.private_key
                                  })
                if sensor == '/sys/bus/w1/devices/28-0000077b5cfd/w1_slave':
                    self.do_redis(sensor,the_temp)

            # Update the readings
            self.readings = dataset
        except Exception as e:

            # `import temp` has probably failed, load test temperatures
            # This should only execute when not on a Pi.

            print('Reverting to test mode:', e)
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
                    print ('Inner fail')# pass #print (r.json())
            except:
                print ('middle fail')
        except Exception as e:
            print ('outer fail')
            #iprint ('Failed to Connect.', e , r.status_code)


        
    def do_redis(self, sensor, temperature):
        try:
            self.redis.set(sensor,temperature )
            self.redis.expire(sensor, 400)
        except redis.exceptions.ConnectionError:
            print('failed to connect to redis.')
 


