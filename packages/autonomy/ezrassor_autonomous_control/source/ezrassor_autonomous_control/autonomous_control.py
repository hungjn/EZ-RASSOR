import rospy
import sys

from std_msgs.msg import Int8, Int16, String
from nav_msgs.msg import Odometry
from gazebo_msgs.msg import LinkStates
from sensor_msgs.msg import JointState
from sensor_msgs.msg import Imu

from numpy import random as r

import ai_objects as obj
import auto_functions as af
import utility_functions as uf

def on_start_up(movement_topic, arms_topic, drums_topic, 
                max_linear_velocity=1, max_angular_velocity=1, 
                real_odometry=False):
    """ Initialization Function  """

    # ROS Node Init Parameters 
    rospy.init_node('autonomous_control', anonymous=True)
    
    #Create Utility Objects
    world_state = obj.WorldState()
    ros_util = obj.ROSUtility(movement_topic, 
                              arms_topic, 
                              drums_topic, 
                              max_linear_velocity, 
                              max_angular_velocity)

    ros_util.status_pub.publish('Spinning Up AI Control')

    # Setup Subscriber Callbacks
    
    if real_odometry:
        rospy.Subscriber('stereo_odometer/odometry', 
                         Odometry, 
                         world_state.odometryCallBack)
    else:
        rospy.Subscriber('/gazebo/link_states', 
                         LinkStates, 
                         world_state.simStateCallBack)
    
    rospy.Subscriber('imu', 
                     Imu, 
                     world_state.imuCallBack)
    rospy.Subscriber('joint_states', 
                     JointState, 
                     world_state.jointCallBack)
    rospy.Subscriber('obstacle_detect', 
                     Int8, 
                     world_state.visionCallBack)
    rospy.Subscriber('routine_toggles', 
                     Int8, 
                     ros_util.autoCommandCallBack)

    result = uf.self_check(world_state, ros_util)

    if result == 2:
        uf.self_right_from_side(world_state, ros_util)
    if result == 3:
        af.auto_dock(world_state, ros_util)

    uf.set_back_arm_angle(world_state, ros_util, 1.5)
    uf.set_front_arm_angle(world_state, ros_util, 1.5)
    
    autonomous_control_loop(world_state, ros_util)

def full_autonomy(world_state, ros_util):
    """ Full Autonomy Loop Function """ 
    
    ros_util.status_pub.publish('Full Autonomy Activated.')

    while(True):
        world_state.target_location.x = r.randint(10,20)
        world_state.target_location.y = r.randint(10,20)
        af.auto_drive_location(world_state, ros_util)
        af.auto_dig(world_state, ros_util, 10)
        af.auto_dock(world_state, ros_util)
    

def autonomous_control_loop(world_state, ros_util):
    """ Control Auto Functions based on auto_function_command input. """

    while(True):

        while ros_util.auto_function_command == 0:
            ros_util.publish_actions('stop', 0, 0, 0, 0)
            ros_util.rate.sleep()

        ros_util.control_pub.publish(True)

        if ros_util.auto_function_command == 1:
            af.auto_drive_location(world_state, ros_util)
        elif ros_util.auto_function_command == 2:
            af.auto_dig(world_state, ros_util, 10)
        elif ros_util.auto_function_command == 4:
            af.auto_dump(world_state, ros_util, 10)
        elif ros_util.auto_function_command == 8:
            uf.self_right_from_side(world_state, ros_util)
        elif ros_util.auto_function_command == 16:
            full_autonomy(world_state, ros_util)
        else:
            ros_util.status_pub.publish('Error Incorrect Auto Function Request {}'
                                        .format(ros_util.auto_function_command))
        
        ros_util.publish_actions('stop', 0, 0, 0, 0)
        ros_util.control_pub.publish(False)