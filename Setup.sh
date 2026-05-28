#!/bin/bash
set -e

echo "Please complete the manual WSL2 and Ubuntu 22.04 setup first. Press enter to continue."
read

sudo apt update && sudo apt upgrade -y

sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

sudo apt install -y software-properties-common curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update && sudo apt upgrade -y
sudo apt install -y ros-humble-desktop
sudo apt install -y ros-dev-tools

echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

source /opt/ros/humble/setup.bash

mkdir -p microros_ws
cd microros_ws

git clone -b humble https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup

sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -y

sudo apt-get install -y python3-pip

colcon build
source install/local_setup.bash

ros2 run micro_ros_setup create_firmware_ws.sh host

ros2 run micro_ros_setup create_agent_ws.sh

ros2 run micro_ros_setup build_agent.sh
source install/local_setup.bash

chmod +x Setup.sh
