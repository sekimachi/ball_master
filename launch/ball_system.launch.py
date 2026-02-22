from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    ball_master = Node(
        package='ball_master',
        executable='ball_master',
        name='ball_master',
        output='screen'
    )

    ball_detector = Node(
        package='ball_detector',
        executable='ball_detector',
        name='ball_detector',
        output='screen'
    )

    ball_operate = Node(
        package='ball_operate',
        executable='ball_operate',
        name='ball_operate',
        output='screen'
    )

    ball_catch = Node(
        package='ball_catch',
        executable='ball_catch',
        name='ball_catch',
        output='screen'
    )

    return LaunchDescription([
        ball_master,
        ball_detector,
        ball_operate,
        ball_catch,
    ])
