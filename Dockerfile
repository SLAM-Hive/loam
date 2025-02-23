FROM osrf/ros:kinetic-desktop-full-xenial

RUN apt-get update \
    && apt-get install -y curl \
    && curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y ros-kinetic-navigation \
    && apt-get install -y ros-kinetic-robot-localization \
    && apt-get install -y ros-kinetic-robot-state-publisher \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt install -y software-properties-common \
    && add-apt-repository -y ppa:borglab/gtsam-release-4.0 \
    && apt-get update \
    && apt install -y libgtsam-dev libgtsam-unstable-dev \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

RUN mkdir -p ~/catkin_ws/src \
    && cd ~/catkin_ws/src
    # && git clone https://github.com/laboshinl/loam_velodyne.git \

COPY loam_velodyne /root/catkin_ws/src/loam_velodyne   

RUN cd ~/catkin_ws \
    && source /opt/ros/kinetic/setup.bash \
    && catkin_make -DCMAKE_BUILD_TYPE=Release \
    && source ~/catkin_ws/devel/setup.bash

RUN echo "source /opt/ros/kinetic/setup.bash" >> /root/.bashrc \
    && echo "source /root/catkin_ws/devel/setup.bash" >> /root/.bashrc

WORKDIR /root/catkin_ws

#RUN apt-get update && apt-get install -y \
#	python3-pip \
#	&& apt-get clean \
#	&& rm -rf /var/lib/apt/lists/* 
#RUN pip3 install pyyaml
#RUN pip3 install rospkg
