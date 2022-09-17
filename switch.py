#!/usr/bin/env python
#encoding: utf8
import sys, rospy
from pimouse_ros.msg import LightSensorValues, SwitchState
from std_srvs.srv import Trigger, TriggerResponse

class Switch():
    def __init__(self):
        self.state = SwitchState()
	self.switch = [False, False]
        self.last_onoff = [False, False]
        self.pub = rospy.Publisher('switch', SwitchState, queue_size=1)
	
    def pub_state(self,num):
	if num == 0:self.state.switch0 = self.switch[0]
	if num == 1:self.state.switch1 = self.switch[1]
	self.pub.publish(self.state)
	print(self.state)

    def update_state(self,s,num):
	onoff = True if s == False else False
        if onoff != self.last_onoff[num]:
	    if(onoff==True):
	        self.switch[num] = onoff ^ self.switch[num]
		self.pub_state(num)
	    self.last_onoff[num] = onoff
        return

if __name__ == '__main__':
    devfile = ['/dev/rtswitch0','/dev/rtswitch1']
    rospy.init_node('switch_check')
    switch = Switch()
    freq = 10
    rate = rospy.Rate(freq)
    while not rospy.is_shutdown():
 	try:
		for i in range(2):
		    with open(devfile[i], 'r') as f:
			s = int(f.readline())
			switch.update_state(s,i)
	except IOError:
	    rospy.logerr("cannot load" + devfile)

	#switch.update_state(s,0)
	rate.sleep()
