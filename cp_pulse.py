#!/usr/bin/env python
#encoding: utf8
import sys, rospy
from pimouse_ros.msg import LightSensorValues, SwitchState, PulseCount
from std_srvs.srv import Trigger, TriggerResponse

class PulseCounter():
    def __init__(self):
        self.count = PulseCount()
	self.devfile = ['/dev/rtcounter_l0','/dev/rtcounter_r0']
        self.pub = rospy.Publisher('pulseconter', PulseCount, queue_size=1)
	#self.sub = rospy.Subscriber('/pulsecounter', PulseCount, self.callback)

    #def callback(self,message):
	#print("got it!")

    def pub_count(self):
	self.pub.publish(self.count)

    def read_count(self):
        r = open(self.devfile[0], 'r')
        self.count.right = int(r.readline())
	r.close()
	l = open(self.devfile[1], 'r')
        self.count.left = int(l.readline())
	l.close()
	#print(self.count)

    def reset_count(self):
        r = open(self.devfile[0], 'w')
        r.write("0")
	r.close()
	l = open(self.devfile[1], 'w')
        l.write("0")
	l.close()

def callback(message):
    print(message)

if __name__ == '__main__':
    devfile = ['/dev/rtcounter_l0','/dev/rtcounter_r0']
    rospy.init_node('pulse_check')
    p = PulseCounter()
    freq = 5
    rate = rospy.Rate(freq)
    pub2 = rospy.Publisher('pulsecounter2', PulseCount, queue_size = 1)
    sub2 = rospy.Subscriber('/pulsecounter2', PulseCount, callback)
    while not rospy.is_shutdown():
	p.read_count()
	p.pub_count()
	pub2.publish(p.count)
	rate.sleep()
    else:
	p.reset_count()

