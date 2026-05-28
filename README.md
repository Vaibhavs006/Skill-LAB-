
**Official Workshop Guide by ASTRA Robotics — RV College of Engineering, Bengaluru**
</div>

---

## About This Guide

This guide is structured as a **multi-session workshop** designed for students getting started with ROS 2 and Micro-ROS. Each session builds on the previous one go through them in order
---

# Environment Setup

## Prerequisites

Before you begin, make sure you have:

- Windows 10 (version 2004 or later) or Windows 11
- At least **4 GB RAM** and **15 GB free disk space**
- A stable internet connection
- **Windows Terminal** — install it from the [Microsoft Store](https://aka.ms/terminal) *(highly recommended)*

---

## Step 0 — Install WSL2 & Ubuntu 22.04

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

This installs WSL2 with Ubuntu by default. If Ubuntu 22.04 isn't set up automatically:

```powershell
wsl --install -d Ubuntu-22.04
```

**Restart your PC** after installation, then launch **Ubuntu 22.04** from the Start menu and set up your Unix username and password.

### Verify WSL Version

In PowerShell:

```powershell
wsl --list --verbose
```

You should see `VERSION 2` next to Ubuntu-22.04. If it shows `VERSION 1`, upgrade it:

```powershell
wsl --set-version Ubuntu-22.04 2
```

> **Tip:** Pin Ubuntu 22.04 to Windows Terminal as your default profile for a smoother experience.

---

## Step 1 — Prepare Ubuntu 22.04

Open your Ubuntu terminal and update the system:

```bash
sudo apt update && sudo apt upgrade -y
```

Set the locale (this is required for ROS 2 to work correctly):

```bash
sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

---

## Step 2 — Add the ROS 2 Repository

Install required tools:

```bash
sudo apt install -y software-properties-common curl gnupg lsb-release
```

Add the ROS 2 GPG key:

```bash
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
```

Add the ROS 2 apt repository:

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

---

## Step 3 — Install ROS 2 Humble

Update apt and install:

```bash
sudo apt update && sudo apt upgrade -y
```

Install the full desktop version (includes RViz, demos, and CLI tools):

```bash
sudo apt install -y ros-humble-desktop
```

>  This takes a few minutes depending on your internet speed. Grab a coffee ☕

Also install the ROS 2 development tools:

```bash
sudo apt install -y ros-dev-tools
```

---

## Step 4 — Configure Your Environment

Add ROS 2 to your shell so it auto-sources on every terminal launch:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Verify Installation

```bash
echo $ROS_DISTRO

```

Expected output:
```
ros2 cli version 0.18.x
```

### Run the Talker–Listener Demo

In your current terminal:

```bash
ros2 run demo_nodes_cpp talker
```

Open a **second terminal** and run:

```bash
ros2 run demo_nodes_py listener
```

You should see the talker publishing `Hello World: X` and the listener receiving it. If that works — **ROS 2 Humble is fully installed!** 🎉

---



## Step 5 — Install Micro-ROS

> **Open a fresh terminal** for this section. Do **not** reuse a terminal from a previous step.

### Source ROS 2

```bash
source /opt/ros/humble/setup.bash
```

### Create the Micro-ROS Workspace

```bash
mkdir microros_ws
cd microros_ws
```

>  **Stay inside `microros_ws`** for all commands in this section until told otherwise.

### Clone the Micro-ROS Setup Repo

```bash
git clone -b humble https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
```

### Update Dependencies

```bash
sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -y
```

### Install pip

```bash
sudo apt-get install python3-pip
```

### Build Micro-ROS Tools

```bash
colcon build
source install/local_setup.bash
```

### Create the Firmware Workspace

```bash
ros2 run micro_ros_setup create_firmware_ws.sh host
```

### Download Micro-ROS Agent Packages

```bash
ros2 run micro_ros_setup create_agent_ws.sh
```

### Build the Agent

```bash
ros2 run micro_ros_setup build_agent.sh
source install/local_setup.bash
```

>  **Note:** Build warnings during these steps are normal — ignore them.

---

# ROS 2 Jazzy on macOS (Apple Silicon) Using Docker

This guide explains how to install and run ROS 2 Jazzy on macOS (Apple Silicon/M-series Macs) using Docker. It also covers GUI applications such as Turtlesim using XQuartz.

---

# Part 1: Install ROS 2 Docker Environment

## Step 1: Install Docker

Download and install Docker Desktop for Apple Silicon (M-series Macs) from Docker's official website.

---

## Step 2: Verify Docker Installation

Check whether Docker is installed correctly.

```bash
docker --version
```

Expected output:

```bash
Docker version xx.x.x
```

---

## Step 3: Pull the ROS 2 Jazzy Base Image

Download the ROS 2 Jazzy Core Docker image.

```bash
docker pull ros:jazzy-ros-core
```

---

## Step 4: Verify Downloaded Images

List all available Docker images.

```bash
docker images
```

You should see:

```bash
ros    jazzy-ros-core
```

---

## Step 5: Create a Project Directory

Create a folder for the ROS Docker setup.

```bash
mkdir ros2_docker
cd ros2_docker
```

---

## Step 6: Create a Dockerfile

Create a Dockerfile.

```bash
touch Dockerfile
```

---

## Step 7: Open the Dockerfile

Open the file using TextEdit.

```bash
open -a TextEdit Dockerfile
```

---

## Step 8: Add Required ROS Packages

Paste the following content into the Dockerfile and save it.

```dockerfile
FROM ros:jazzy-ros-core

RUN apt-get update && apt-get install -y \
    ros-jazzy-demo-nodes-cpp \
    ros-jazzy-foxglove-bridge \
    ros-jazzy-tf2-ros
```

### Package Explanation

| Package | Purpose |
|----------|----------|
| ros-jazzy-demo-nodes-cpp | ROS 2 demo publisher/subscriber examples |
| ros-jazzy-foxglove-bridge | Connect ROS 2 with Foxglove Studio |
| ros-jazzy-tf2-ros | Coordinate frame transformations |

---

## Step 9: Build the Docker Image

Build a custom image named `rosdemo`.

```bash
docker build -t rosdemo .
```

---

## Step 10: Run the Container

Launch the container and open a shell.

```bash
docker run --rm -it rosdemo bash
```

---

# Part 2: Enable GUI Applications with XQuartz

ROS GUI applications such as Turtlesim require an X11 display server.

---

## Step 1: Install XQuartz

Download and install XQuartz.

After installation, restart your Mac if required.

---

## Step 2: Allow Network Connections

Open:

```text
XQuartz → Settings → Security
```

Enable:

```text
Allow connections from network clients
```

---

# Part 3: Create a GUI-Enabled ROS 2 Container

## Step 1: Create the Container

Create a persistent ROS 2 container with GUI support.

```bash
docker run -itd \
  --name ros2_jazzy \
  -e DISPLAY=host.docker.internal:0 \
  ros:jazzy
```

### Explanation

| Option | Description |
|----------|----------|
| -itd | Interactive + terminal + detached mode |
| --name ros2_jazzy | Container name |
| DISPLAY=host.docker.internal:0 | Sends GUI output to XQuartz |

---

## Step 2: Start the Container

Whenever you want to use ROS 2 again:

```bash
docker start ros2_jazzy
```

---

## Step 3: Enter the Container

Open a shell inside the running container.

```bash
docker exec -it ros2_jazzy bash
```

---

## Step 4: Install Required ROS Packages

Update package lists and install GUI-related ROS packages.

```bash
apt update

apt install -y \
  ros-jazzy-turtlesim \
  ros-jazzy-rqt-graph \
  ros-jazzy-demo-nodes-cpp \
  ros-jazzy-foxglove-bridge
```

### Package Explanation

| Package | Purpose |
|----------|----------|
| ros-jazzy-turtlesim | ROS learning simulator |
| ros-jazzy-rqt-graph | Visualize ROS node connections |
| ros-jazzy-demo-nodes-cpp | Demo publisher/subscriber nodes |
| ros-jazzy-foxglove-bridge | Connect to Foxglove Studio |

---

## Step 5: Source ROS 2

Load the ROS 2 environment.

```bash
source /opt/ros/jazzy/setup.bash
```

---

# Part 4: Running Turtlesim

Turtlesim is a simple simulator used for learning ROS concepts such as nodes, topics, and publishers/subscribers.

---

## Step 1: Allow XQuartz Access

Open a terminal on macOS and run:

```bash
xhost +localhost
```

---

## Step 2: Enter the Container

Start the container and open a shell.

```bash
docker start ros2_jazzy

docker exec -it ros2_jazzy bash
```

---

## Step 3: Source ROS 2

```bash
source /opt/ros/jazzy/setup.bash
```

---

## Step 4: Verify Turtlesim Installation

List available turtlesim executables.

```bash
ros2 pkg executables turtlesim
```

You should see executables such as:

```bash
turtlesim_node
draw_square
mimic
```

---

## Step 5: Launch Turtlesim

Start the turtlesim GUI.

```bash
ros2 run turtlesim turtlesim_node
```

A window containing a turtle should appear.

---

## Step 6: Open Another Terminal

Enter the running container again.

```bash
docker exec -it ros2_jazzy bash
```

---

## Step 7: Source ROS 2

```bash
source /opt/ros/jazzy/setup.bash
```

---

## Step 8: Start the Keyboard Controller

Launch the teleoperation node.

```bash
ros2 run turtlesim turtle_teleop_key
```

---

## Step 9: Control the Turtle

Use the keyboard arrow keys:

| Key | Action |
|-------|---------|
| ↑ | Move forward |
| ↓ | Move backward |
| ← | Rotate left |
| → | Rotate right |

You should now be able to control the turtle inside the Turtlesim window.

---

# Useful Docker Commands

## List Running Containers

```bash
docker ps
```

---

## List All Containers

```bash
docker ps -a
```

---

## Stop the Container

```bash
docker stop ros2_jazzy
```

---

## Restart the Container

```bash
docker start ros2_jazzy
```

---

## Enter the Container

```bash
docker exec -it ros2_jazzy bash
```

---

# Expected Outcome

After completing this guide, you will have:

- ROS 2 Jazzy running inside Docker
- GUI applications working through XQuartz
- Turtlesim running successfully
- Keyboard control of the turtle
- A reusable ROS 2 development environment on macOS (Apple Silicon)

---

## Troubleshooting

###  `wsl --install` doesn't work
- Enable **Virtualization** in your BIOS/UEFI settings
- Run PowerShell strictly as **Administrator**
- Make sure Windows is updated to the latest version

---

###  Locale errors during ROS 2 install
Re-run the locale commands from Step 1:
```bash
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
```

---

###  `ros2: command not found`
ROS 2 wasn't sourced. Fix it permanently:
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && source ~/.bashrc
```

---

###  `rosdep: command not found`
```bash
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
```

---

###  `colcon: command not found`
```bash
sudo apt install python3-colcon-common-extensions
```

---

###  `E: Unable to locate package ros-humble-desktop`
The ROS 2 repository wasn't added correctly. Redo Step 2, then:
```bash
sudo apt update
sudo apt install ros-humble-desktop
```

---

### Micro-ROS `create_firmware_ws.sh` fails
Ensure you're inside `microros_ws` and have sourced both files:
```bash
source /opt/ros/humble/setup.bash
source install/local_setup.bash
```

---

### WSL has no internet access
```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

To make this permanent across reboots:
```bash
echo -e "[network]\\ngenerateResolvConf = false" | sudo tee /etc/wsl.conf
```

---

###  `colcon build` crashes or freezes (out of memory)
Limit parallel workers:
```bash
colcon build --parallel-workers 1
```

---

##  Quick Command Reference

| Task | Command |
|---|---|
| Source ROS 2 | `source /opt/ros/humble/setup.bash` |
| Source local workspace | `source install/local_setup.bash` |
| Check ROS 2 version | `ros2 --version` |
| List active nodes | `ros2 node list` |
| List topics | `ros2 topic list` |
| Echo a topic | `ros2 topic echo /topic_name` |
| Build workspace | `colcon build` |
| Build (low memory) | `colcon build --parallel-workers 1` |

---


## References

- [ROS 2 Humble — Official Installation Docs](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
- [Micro-ROS Setup — GitHub](https://github.com/micro-ROS/micro_ros_setup)
- [WSL2 — Microsoft Docs](https://learn.microsoft.com/en-us/windows/wsl/)
- [ASTRA Robotics](https://github.com/AstraRobotics)
