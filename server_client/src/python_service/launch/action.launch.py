import launch
import launch.launch_description_sources
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    action_declare_startup_rqt = launch.actions.DeclareLaunchArgument(
        'startup_rqt', default_value="False"
    )
    start_rqt = launch.substitutions.LaunchConfiguration('starup_rqt', default="False")
    multisim_launch_path = [get_package_share_directory('turtlesim'),'launch/','multisim.launch.py']
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            multisim_launch_path
        )
    )
    # 打印数据
    action_log_info = launch.actions.LogInfo(str(multisim_launch_path))
    # 执行进程， 执行一个命令行
    action_topic_list = launch.actions.ExecuteProcess(
        condition = launch.conditions.IfCondition(start_rqt), 
        cmd=['ros2','topic','list', '&', 'rqt']
    )
    # 组织动作成组， 把多个动作放到一组
    action_group = launch.actions.GroupAction([
        launch.actions.TimerAction(period=2.0, actions=[action_include_launch]),
        launch.actions.TimerAction(period=2.0, actions=[action_topic_list]),
        
    ])
    return launch.LaunchDescription([
        # action 动作
        action_topic_list,
        action_group
    ])