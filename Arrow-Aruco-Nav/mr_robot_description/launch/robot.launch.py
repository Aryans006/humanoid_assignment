#! /usr/bin/env python3
import xacro
from os.path import join
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument, TimerAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, Command, PythonExpression
from launch.conditions import IfCondition
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
    
    xacro_file=get_package_share_directory('mr_robot_description')+'/urdf/mr_robot.xacro'
    bridge_config=get_package_share_directory('mr_robot_description')+ '/config/bridge.yaml'
    rviz_config=get_package_share_directory("mr_robot_description")+"/config/rviz_config.rviz"
    #publishing robot_state into topic robot_description
    robot_state=Node(package = 'robot_state_publisher',
                            executable = 'robot_state_publisher',
                            name='robot_state_publisher',
                            parameters = [{'robot_description': ParameterValue(Command( \
                                        ['xacro ', xacro_file,
                                        # ' kinect_enabled:=', "true",
                                        # ' lidar_enabled:=', "true",
                                        # ' camera_enabled:=', camera_enabled,
                                        ]), value_type=str)}]
                            )
    
    #spawn mr_robot using the topic "/mr_robot_description"
    robot_spawn=Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
                    '-name', 'mr_robot',
                    '-topic', '/robot_description',
                    "-allow_renaming", "true",
                    '-x', '0.0',  # Set the initial X position
                    '-y', '0.0',  # Set the initial Y position
                    '-z', '0.0' ,  # Set the initial Z position
                    '-Y', '0.0'   # Set the initial Z position
                    # '-x', '2.0',  # Set the initial X position
                    # '-y', '0.0',  # Set the initial Y position
                    # '-z', '0.0' ,  # Set the initial Z position
                    # '-Y', '-1.57'   # Set the initial Z position
    ]
    )

    # parameter bridge node to bridge different gz and tos 2 topics
    ros_gz_bridge = Node(
                package="ros_gz_bridge", 
                executable="parameter_bridge",
                parameters = [
                    {'config_file': bridge_config}],
                # condition=IfCondition(with_bridge)
                )
    
    # ros_gz_image_bridge = Node(
    #     package="ros_gz_image" ,
    #     executable="image_bridge" , 
    #     arguments=("/camera/image_raw")  
    # )
    
    # launch rviz node if rviz parameter was set to true
    rviz = Node(package='rviz2',
                executable='rviz2',
                name='rviz',
    #				output='screen',
                arguments=['-d' + rviz_config],
                # condition=IfCondition(with_rviz)
                )
    # map_stf = Node(package="tf2_ros",
    #                executable="static_transform_publisher",
    #                arguments=["0","0","0","0.0","0.0","0.0","map","odom"])
    
    arg_use_sim_time = DeclareLaunchArgument('use_sim_time',
											default_value='true',
											description="Enable sim time from /clock")
    
    return LaunchDescription([
        arg_use_sim_time,
        robot_state,
        robot_spawn,
        ros_gz_bridge,
        rviz,
        # ros_gz_image_bridge ,
        # map_stf
        # arg_with_bridge
    ])