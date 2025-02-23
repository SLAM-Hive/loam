import yaml, time, subprocess
from string import Template
# Generate mappingtask.yaml according to template.yaml and config.yaml
config_raw = open("/slamhive/config.yaml",'r',encoding="UTF-8").read()
config_dict = yaml.load(config_raw, Loader=yaml.FullLoader)

# Read algorithm-parameters and algorithm-remap from config.yaml for launch

algo_parameters_dict = config_dict["algorithm-parameters"]
algo_parameters_list = []
if(algo_parameters_dict is not None):
    for key, value in algo_parameters_dict.items():
        algo_parameters_list.append(key + ":=" + str(value))
algo_parameters = ' '.join(algo_parameters_list)

algo_remap_dict = config_dict["algorithm-remap"]
algo_remap_list = []
if(algo_remap_dict is not None):
    for key, value in algo_remap_dict.items():
        algo_remap_list.append(key + ":=" + str(value))
algo_remap = ' '.join(algo_remap_list)
# roslaunch_command = "roslaunch loam_velodyne loam_velodyne.launch rviz:=false " + algo_parameters + " " + algo_remap
roslaunch_command = "roslaunch /slamhive/loam_velodyne.launch rviz:=false " + algo_parameters + " " + algo_remap


general_dict = config_dict["general-parameter"]
save_map = False
if general_dict is not None:
    for key, value in general_dict.items():
        if key == "save_map":
            if value == 1 or value == "1":
                save_map = True


time.sleep(1)

subprocess.run("bash -c 'source /opt/ros/kinetic/setup.bash;  \
                source /root/catkin_ws/devel/setup.bash; "
                + roslaunch_command 
                + " & sleep 10s ;'", shell=True)


subprocess.Popen("bash -c 'source /opt/ros/kinetic/setup.bash;  \
                source /root/catkin_ws/devel/setup.bash; "
                + " mkdir /root/catkin_ws/pcd ;\
                cd /root/catkin_ws/pcd ;\
                rosrun pcl_ros pointcloud_to_pcd input:=laser_cloud_surround;'", shell=True)

# 不需要监控了，直接保存整个文件夹
# subprocess.Popen("bash -c 'source /opt/ros/kinetic/setup.bash;  \
#                source /root/catkin_ws/devel/setup.bash; "
#                + " python3 /slamhive/pcd_monitor.py'", shell=True)
#
subprocess.run("bash -c 'source /opt/ros/kinetic/setup.bash;  \
                source /root/catkin_ws/devel/setup.bash; \
                python3 /slamhive/dataset/rosbag_play.py; \
                rosnode kill -a ; \
                sleep 5s ; \
                mv /root/catkin_ws/traj.txt /slamhive/result/traj.txt;'", shell=True)

if save_map :
    subprocess.run("bash -c 'cp -r /root/catkin_ws/pcd /slamhive/result/pcd;'", shell=True)
subprocess.run("bash -c 'touch /slamhive/result/finished ;'", shell=True)































































































































































