
import logging
from time import sleep
from ev3_robot_car import SensorUltrasonic, SensorInfrared

def write_to_csv(csv_file, values):
    logf = open(csv_file,"w") # overwrite values
    for val in values:
        try:
            logf.write(str(val))
            logf.write(",")
            logf.write("\r\n")
        except OSError:
            print("Disk full?")
    logf.close()


if __name__ == '__main__':
    """measure values for the specified sensors multiple times; store measures as .csv file
    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info('SENSOR TEST START')

    ##################### CREATE SENSORS #####################
    inputs = {}
    #ultrasonic left/west
    sensor_pos = 'west'
    sensor = SensorUltrasonic('in1', )
    inputs.update({sensor_pos: sensor})
    #ultrasonic right/east
    sensor_pos = 'east'
    sensor = SensorUltrasonic('in4')
    inputs.update({sensor_pos: sensor})
    #ultrasonic up/north
    sensor_pos = 'north'
    sensor = SensorInfrared('in2')
    inputs.update({sensor_pos: sensor})

    ##################### MEASURE SENSOR VALUES #####################
    n_measures = 30

    for sensor_pos, sensor in inputs.items():
        #measure values
        measurements = []
        for i in range(n_measures):
            value = sensor.read()
            logging.info('READ (%s)    # %s  :  VALUE (%s)', sensor.port + '_' + sensor_pos, str(i), str(value) )
            measurements.append(value)
            sleep(0.05)

        #store values as csv file
        file_path = 'measures_'+sensor.port+'_'+sensor_pos+".csv"
        write_to_csv(file_path, measurements)

        