import launch
import launch_ros

# ros2 run turtlesim turtle_teleop_key 
def generate_launch_description():
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument(
        'launch_arg_bg',default_value=150
    )
    """
    产生launch描述
    """
    action_node_turtlesim = launch_ros.actions.Node(
        package="turtlesim",
        executable="turtlesim",
        parameters=[{'background_g':launch.substitutions.LaunchConfiguration(
            'launch_arg_bg',default="150"
        )}],
        output="screen"
    )
    
    action_node_face_detect = launch_ros.actions.Node(
        package="python_service",
        executable="face_node",
        output="log"
    )
    
    return launch.LaunchDescription([
        action_node_turtlesim,
        action_node_face_detect
    ])
#ros2 launch package demo.launch.py