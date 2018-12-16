sensors = ['/sys/bus/w1/devices/28-0000077aae57/w1_slave',
           '/sys/bus/w1/devices/28-0000077aa8d5/w1_slave',
           '/sys/bus/w1/devices/28-0000077b5cfd/w1_slave',
           ]

r = Report('http://192.168.2.23:5000/temperature/temp', sensors )

count = 0
while True:
    
    print ('-> Reading temperature ...')
    r.read_temps()
    print ('-> Submitting Temperatures ...')
    r.submit()
    print ('-> Items in Queue: ', len(r.readings))
    sleep(60)


print ('done')
