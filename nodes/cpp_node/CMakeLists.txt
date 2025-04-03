cmake_minimum_required(VERSION 3.8)
project(cpp_node)
add_executable(cpp_node ros2_node_cpp.cpp)

find_package(rclcpp REQUIRED)   # 直接查找找到对应的头文件和库文件
message(STATIC ${rclcpp_INCLUDE_DIRS})  # 头文件及rclcpp依赖的头文件
message(STATIC ${rclcpp_LIBRARIES})     # 库文件及rclcpp依赖的库文件

target_include_directories(cpp_node PUBLIC ${rclcpp_INCLUDE_DIRS})
target_link_libraries(cpp_node ${rclcpp_LIBRARIES})