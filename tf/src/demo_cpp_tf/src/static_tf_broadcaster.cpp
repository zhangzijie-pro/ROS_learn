#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "tf2_ros/static_transform_broadcaster.h"

class StaticTFBroadcaster: public rclcpp::Node
{
private:

public:
    StaticTFBroadcaster():Node("static_tf_broadcaster")
    {
        
    }
}