#!/usr/bin/env python
#encoding: utf8

def exec_music(goal):
    r = MusicResult()
    fb = MusicFeedback()

    for i, f in enumerate(goal.freqs):
	fb.remaining_steps = len(goal.freqs) - i
	music.publish_feedback(fb)

	if music.is_preempt_requested():
	    write_freq(0)
	    r.finished = False
	    music.set_preempted(r)
	    return

	write_freq(f)
	rospy.sleep(1.0 if i >= len(goal.durations) else goal.durations[i])

    r.finished = True
    music.set_succeeded(r)
