import rospy
from visualization_msgs.msg import Marker, MarkerArray


rospy.init_node('markers_viz')
markers_arr_pub = rospy.Publisher("/visualization_marker", Marker, queue_size=1)

def pub_marker():
    marker = Marker()

    marker.header.frame_id = "base_link"
    marker.header.stamp = rospy.Time.now()
    marker.ns = "my_marker"
    marker.id = 1
    marker.type =  Marker.CUBE
    marker.action = Marker.ADD
    marker.pose.position.x = 1.0
    marker.pose.position.y = 1.0
    marker.pose.position.z = 0.0
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.scale.x = 1.0
    marker.scale.y = 1.0
    marker.scale.z = 1.0

    marker.color.a = 1.0
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0

    markers_arr_pub.publish(marker)
    print(marker)
    print('success')

pub_marker()