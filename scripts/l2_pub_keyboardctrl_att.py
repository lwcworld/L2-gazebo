#!/usr/bin/env python
import math
import rospy
import std_msgs.msg
from geometry_msgs.msg import PoseStamped, Quaternion
from std_msgs.msg import Float64

class agent(object):
    def __init__(self):
        self.pub_att = rospy.Publisher('/mavros/setpoint_attitude/attitude', PoseStamped, queue_size=10)
        self.pub_thr = rospy.Publisher('/mavros/setpoint_attitude/att_throttle', Float64, queue_size=10)
        self.cmd_att = PoseStamped()

        self.count = 1
        self.v = [1.0, 0.0, 0.0]
        self.v_norm = math.sqrt(self.v[0]**2 + self.v[1]**2 + self.v[2]**3)
        self.theta = 0

        self.cmd_thr = Float64()
        self.cmd_thr.data = 0.3

    def calc_cmd_att_thr(self):
        self.cmd_att.header.stamp = rospy.Time.now()
        # self.cmd_att.header.seq = self.count
        # self.cmd_att.header.frame_id = 1
        self.cmd_att.pose.position.x = 0.0
        self.cmd_att.pose.position.y = 0.0
        self.cmd_att.pose.position.z = 10.0

        self.cmd_att.pose.orientation.x = math.sin(self.theta / 2.0) * self.v[0] / self.v_norm;
        self.cmd_att.pose.orientation.y = math.sin(self.theta / 2.0) * self.v[1] / self.v_norm;
        self.cmd_att.pose.orientation.z = math.sin(self.theta / 2.0) * self.v[2] / self.v_norm;
        self.cmd_att.pose.orientation.w = math.cos(self.theta / 2.0);

        self.count += 1
        self.theta = 0.3*math.sin(self.count/300.0)

        return (cmd_att, cmd_thr)

    def talk(self):
        # print(self.theta)
        self.pub_att.publish(self.cmd_att)
        self.pub_thr.publish(self.cmd_thr)
        rospy.loginfo("[cmd req] pos : %s, %s, %s || att : %s, %s, %s, %s", self.cmd_att.pose.position.x, self.cmd_att.pose.position.y, self.cmd_att.pose.position.z, self.cmd_att.pose.orientation.x, self.cmd_att.pose.orientation.y, self.cmd_att.pose.orientation.z, self.cmd_att.pose.orientation.w)

if __name__ == '__main__':
    rospy.init_node('l2_pub_keyboardctrl_att')

    # pub_att = rospy.Publisher('/mavros/setpoint_attitude/attitude', geometry_msgs.msg.PoseStamped, queue_size=100)
    # pub_thr = rospy.Publisher('/mavros/setpoint_attitude/att_throttle', std_msgs.msg.Float64, queue_size=100)

    rate = rospy.Rate(10) # 10Hz

    cmd_att = PoseStamped()
    cmd_thr = std_msgs.msg.Float64

    agent1 = agent()


    while not rospy.is_shutdown():
        try:
            agent1.calc_cmd_att_thr()
            agent1.talk()
            rate.sleep()

        except rospy.ROSInterruptException:
            pass