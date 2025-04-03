#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <chrono>
#include <turtlesim/msg/pose.hpp>

using namespace std::chrono_literals;

class ControlNode: public rclcpp::Node
{
private:
    //rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscription_;
    double target_x_{1.0};
    double target_y_{1.0};
    double k_{1.0}; // 比例系数
    double max_speed_{3.0};

public:
    ControlNode(const std::string &node_name): Node(node_name)
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel",10);
        subscription_ = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose",10, 
            std::bind(&ControlNode::one_pose_received, this, std::placeholders::_1));
    }

   void one_pose_received(const turtlesim::msg::Pose::SharedPtr pose){
        auto msg = geometry_msgs::msg::Twist();

        auto current_x = pose->x;
        auto current_y = pose->y;
        
        RCLCPP_INFO(get_logger(),"当前位置为%f, %f",current_x,current_y);

        auto distance = std::sqrt(
            (target_x_-current_x)*(target_x_-current_x)+
            (target_y_-current_y)*(target_y_-current_y)
        );

        auto angle = std::atan2((target_y_-current_y),(target_x_-current_x))-pose->theta;

        if(distance>0.1){
            if(fabs(angle)>0.2){
                msg.angular.z = fabs(angle);
            }else{
                msg.linear.x = std::min(k_*distance,max_speed_);
            }
        }

        publisher_->publish(msg);
   }
};

int main(int argv, char *argc[]){
    rclcpp::init(argv, argc);
    auto node = std::make_shared<ControlNode>("control_node_cpp");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}