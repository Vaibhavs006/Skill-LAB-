
**Official Workshop Guide by ASTRA Robotics — RV College of Engineering, Bengaluru**
</div>

---

## About This Guide

This guide is structured as a **multi-session workshop** designed for students getting started with ROS 2 and Micro-ROS. Each session builds on the previous one — go through them in order
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
ros2 --version
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
