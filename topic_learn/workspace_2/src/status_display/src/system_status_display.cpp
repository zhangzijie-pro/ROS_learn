#include <QString>
#include <QApplication>
#include <QLabel>
#include <rclcpp/rclcpp.hpp>
#include <status_interface/msg/system_status.hpp>

using SystemStatus = status_interface::msg::SystemStatus;

class SysStatusDisplay:public rclcpp::Node
{
private:
    rclcpp::Subscription<SystemStatus>::SharedPtr Subscriptier_;
    QLabel *label_;
    /* data */
public:
    SysStatusDisplay(/* args */):Node("sys_status_display")
    {
        label_ = new QLabel();
        Subscriptier_ = this->create_subscription<SystemStatus>("SystemStatus",10,
        [&](const SystemStatus::SharedPtr msg)->void{
            label_->setText(qstr_from_msg(msg));
        });

        label_->setText(
            qstr_from_msg(std::make_shared<SystemStatus>())
        );
        label_->show();

    };

    QString qstr_from_msg(const SystemStatus::SharedPtr msg){
        std::stringstream show_str;
        show_str << 
        "===========系统状态显示===========\n"<<
        "显示时间\t" << msg->stamp.sec << "\ts\n"<<
        "主机名字\t" << msg->host_name << "\t\n"<<
        "CPU占用率\t" << msg->cpu_percent << "\t%\n"<<
        "内存占用率\t" << msg->memory_percent << "\t%\n"<<
        "总内存\t" << msg->memory_total << "\tMB\n"<<
        "剩余内存\t" << msg->memory_available << "\tMB\n"<<
        "发送数据量\t" << msg->net_sent << "\tMB\n"<<
        "接受数据量\t" << msg->net_recv << "\tMB\n" <<
        "================================";

        return QString::fromStdString(show_str.str());
    };
};


int main(int argc, char *argv[]){
    rclcpp::init(argc,argv);
    QApplication app(argc,argv);
    auto node = std::make_shared<SysStatusDisplay>();
    std::thread spin_thread([&]()->void{
        rclcpp::spin(node);
    });
    spin_thread.detach();
    app.exec();
    return 0;
}