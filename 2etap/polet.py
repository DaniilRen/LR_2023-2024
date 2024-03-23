import rospy
import math
from clover import srv
from mavros_msgs.srv import CommandBool 
from std_srvs.srv import Trigger 
from std_msgs.msg import Float64

navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global =rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
land = rospy.ServiceProxy('land', Trigger)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
get_telemetry =rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)


rospy.init_node('polet')


def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=1.5, frame_id='aruco_map_detected', auto_arm=False, tolerance=0.2):
    navigate(x=x,y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)
    while not rospy.is_shutdown():
        telemetry = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telemetry.x ** 2 + telemetry.y** 2 + telemetry.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)
    

def count_victims(point, victims):
    cnt = 0
    for v in victims:
        x1, y1 = point[:2]
        x2, y2 = v[:2]
        if math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) <= 2.5:
            cnt += 1
    return cnt


def read_input_data():
    boxes_data = [float(i) for i in input().strip()[1:-1].replace(')', '').replace('(', '').replace(',', '').split()]
    boxes = []
    box = []
    for i in range(1, len(boxes_data)+1):
        if i % 3 == 0:
            box.append(boxes_data[i-1])
            boxes.append(box)
            box = []
            continue
        box.append(boxes_data[i-1])

    victims_input = input().strip()[1:-1].replace(')', '').replace('(', '').replace(',', '').split()
    victims = []
    v = []
    for i in range(1, len(victims_input)+1):
        if i % 3 == 0:
            v.append(victims_input[i-1])
            victims.append(v)
            v = []
            continue
        v.append(float(victims_input[i-1]))

    return boxes, victims


def print_data(sens, cords, victims_count):
    for i in range(len(sens)):
        print(f'{i+1}. {cords[i]} = {sens[i]}, {victims_count[i]}')


cords, victims = read_input_data()
sensor = []
victims_count = []
 

navigate_wait(z=2.0,frame_id='body', speed=3.0,auto_arm=True)

print('Start navigating')
for point in cords:

    navigate_wait(x=point[0], y=point[1], z=point[2] + 0.5)
    rospy.sleep(7)

    land()
    rospy.sleep(3)

    arming(False)
    rospy.sleep(5)
    print('landed')

    sensor_data = rospy.wait_for_message('/sensor', Float64)
    data = sensor_data.data
    sensor.append(data)
    victims_count.append(count_victims(point, victims))
    print('counted data')

    rospy.sleep(5)

    arming(True)
    navigate_wait(z=1.0, frame_id='body', yaw=float('nan'), speed=3.0, auto_arm=True)
    rospy.sleep(7)
    if point[2] >= 3:
        print('correcting coordinates')
        if point[0] <= 5:
            navigate_wait(x=1.5, frame_id='body', speed=2.5)
        else:
            navigate_wait(x=-1.5, frame_id='body', speed=2.5)
        rospy.sleep(2)
        navigate_wait(z=-1.5, frame_id='body', speed=2.5)
    rospy.sleep(5)

    
navigate_wait(x=0, y=0, z=1.0)
land()
print_data(sensor, cords, victims_count)