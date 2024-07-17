import os

import launch
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    main_param_dir = launch.substitutions.LaunchConfiguration(
        'main_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'param', 'lidarslam_hesai_outdoor_okinawa.yaml'));
    
    rviz_param_dir = launch.substitutions.LaunchConfiguration(
        'rviz_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'rviz',
            'mapping_bhxqd1yhy_china.rviz'))

    mapping = launch_ros.actions.Node(
        package='scanmatcher',
        executable='scanmatcher_node',
        parameters=[main_param_dir],
        remappings=[('/input_cloud','/sensing/lidar/top/hesai_points')],
        output='screen'
        )


    graphbasedslam = launch_ros.actions.Node(
        package='graph_based_slam',
        executable='graph_based_slam_node',
        parameters=[main_param_dir],
        output='screen'
        )
    

    """
        x: 1.01
        y: 0.0
        z: 0.93
        roll: 0.0
        pitch: 0.0
        yaw: 0.0

    """
    tf = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['1.0','0.0','0.93','0','0','0','1','base_link','hesai_top_base_link']
        )

    """
    tamagawa/imu_link:        # Okinawa testbed center
        x: -0.5
        y: 0.0
        z: -0.50
        roll: 0.0
        pitch: 0.0
        yaw: 0.0
    """

    tf_imu = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0.51','0','0.43','0','0','0','1','base_link','tamagawa/imu_link']
        )


    rviz = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_param_dir]
        )


    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'main_param_dir',
            default_value=main_param_dir,
            description='Full path to main parameter file to load'),
        mapping,
        graphbasedslam,
        tf, tf_imu,
        rviz,
            ])
