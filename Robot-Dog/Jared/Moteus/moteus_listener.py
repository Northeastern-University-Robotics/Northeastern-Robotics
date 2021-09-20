#!/usr/bin/env python
# license removed for brevity


from asyncio import queues
import rospy
import moteus
from std_msgs.msg import String
import asyncio
from threading import Thread
import math
from sensor_msgs.msg import JointState
from Jared.msg import simpleMoteus

exitFlag = False
moteus_thread = None

position = 0
velocity = 0
torque = 0

def chatter_callback(message):
    global position, velocity, torque
    position = message.position
    velocity = message.velocity
    torque = message.torque
    #print("Moving to positon: " + str(position))
    #rospy.loginfo(rospy.get_caller_id() + "Recieved Message: %s", message.data)
    pass

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('chatter', simpleMoteus, chatter_callback)

    rospy.spin()
    

def moteusMain(threadName):
    global exitFlag, position, velocity, torque

    def createEventLoop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return asyncio.get_event_loop()

    loop = createEventLoop()
    asyncio.set_event_loop(loop)

    async def onClose(c:moteus.Controller=None):
        #Shut down motor procedure
        pass

    async def onOpen(c:moteus.Controller=None):
        await c.set_rezero()

    async def main():
        c = moteus.Controller()

        await onOpen(c=c)

        while not exitFlag:
            state = await c.set_position(position=position, velocity=velocity, maximum_torque=torque ,query=True)
            #print(state)
            #print("Position:", state.values[moteus.Register.POSITION])
            #print()
            #print(position, state.values[moteus.Register.POSITION])
            rospy.loginfo("Moving to pos: " + str(round(position, 3)) + ". At pos: " + str(round(state.values[moteus.Register.POSITION], 3)))
            await asyncio.sleep(0.02)

        await onClose()

    asyncio.run(main())

def closeMoteus():
    global exitFlag
    exitFlag = True
    moteus_thread.join()

if __name__ == '__main__':
    moteus_thread = Thread(target=moteusMain, args=(0,))
    moteus_thread.start()
    rospy.on_shutdown(closeMoteus)
    listener()


