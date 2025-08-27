#!/usr/bin/env python3
from std_msgs.msg import String
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class MyNode(Node):
    def __init__(self):
        super().__init__('node_name')
        self.shoulder_pitch = self.create_publisher(Float64, '/LShoulderPitch/cmd_pos', 10)
        self.shoulder_roll = self.create_publisher(Float64, '/LShoulderRoll/cmd_pos', 10)
        self.elbow_yaw = self.create_publisher(Float64, '/LElbowYaw/cmd_pos', 10)
        self.elbow_roll = self.create_publisher(Float64, '/LElbowRoll/cmd_pos', 10)
        self.ShoulderPitch = Float64()
        self.ShoulderRoll = Float64()
        self.ElbowYaw = Float64()

        self.wave()
        self.reset()
        self.point()
        self.reset()
        self.grasp()
        self.reset()


    def wave(self):
        print("Waving")
        self.ShoulderPitch.data = -2.08
        self.shoulder_pitch.publish(self.ShoulderPitch)
        print("Wave ")
        for i in range (3):
            self.ElbowYaw.data = -0.78
            self.elbow_roll.publish(self.ElbowYaw)
            time.sleep(1)
            self.ElbowYaw.data = -0.03
            self.elbow_roll.publish(self.ElbowYaw)
            time.sleep(1)
            i =+ 1


    
    def point(self):
        print("Pointing")
        msg = Float64()
        msg.data = -1.13
        self.shoulder_pitch.publish(msg)
        time.sleep(4)
    
    def grasp(self):
        print("Grasping")
        msg = Float64()
        msg.data = -1.19
        self.shoulder_pitch.publish(msg)
        msg.data = -1.16
        self.elbow_roll.publish(msg)
        msg.data = 1.28
        self.shoulder_roll.publish(msg)
        time.sleep(2)
        msg.data = -0.67
        self.shoulder_pitch.publish(msg)
        time.sleep(2)
        msg.data = -2.08
        self.shoulder_pitch.publish(msg)
        time.sleep(3)
        
    
    def reset(self):
        print("Resetting")
        msg = Float64()
        lsp = 0.0
        lsr = 0.0
        ley = 0.0
        ler = -0.03
        msg.data = lsp
        self.shoulder_pitch.publish(msg)
        msg.data = lsr
        self.shoulder_roll.publish(msg)
        msg.data = ley
        self.elbow_yaw.publish(msg)
        msg.data = ler
        self.elbow_roll.publish(msg)
        time.sleep(3)


def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()