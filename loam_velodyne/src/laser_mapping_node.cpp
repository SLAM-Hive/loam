#include <ros/ros.h>
#include "loam_velodyne/LaserMapping.h"


// void path_save(nav_msgs::Odometry odomAftMapped ){
 
// 	    //保存轨迹，path_save是文件目录,txt文件提前建好,/home/xxx/xxx.txt,
//    			std::ofstream pose1("/root/catkin_ws/traj.txt", std::ios::app);
// 			pose1.setf(std::ios::scientific, std::ios::floatfield);
// 			pose1.precision(9);
	
// 			static double timeStart = odomAftMapped.header.stamp.toSec();
// 			auto T1 =ros::Time().fromSec(timeStart) ;
// 			pose1<< odomAftMapped.header.stamp -T1<< " "
//               << -odomAftMapped.pose.pose.position.y << " "
//               << odomAftMapped.pose.pose.position.z << " "
//               << odomAftMapped.pose.pose.position.x << " "
//               << odomAftMapped.pose.pose.orientation.x << " "
//               << odomAftMapped.pose.pose.orientation.y << " "
//               << odomAftMapped.pose.pose.orientation.z << " "
//               << odomAftMapped.pose.pose.orientation.w << std::endl;
// 			pose1.close();
            
// }

/** Main node entry point. */
int main(int argc, char **argv)
{
  ros::init(argc, argv, "laserMapping");
  ros::NodeHandle node;
  ros::NodeHandle privateNode("~");

  loam::LaserMapping laserMapping(0.1);


  /***********  save path **********/
  //ros::Subscriber save_path = node.subscribe<nav_msgs::Odometry>("/aft_mapped_to_init",     100, path_save);

  if (laserMapping.setup(node, privateNode)) {
    // initialization successful
    laserMapping.spin();
  }

  return 0;
}
