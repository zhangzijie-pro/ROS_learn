#include <QString>
#include <QApplication>
#include <QLabel>

int main(int argc, char *argv[]){
    QApplication app(argc,argv);
    QLabel* label = new QLabel();
    QString message = QString::fromStdString("Hello qt");
    label->setText(message);
    label->show();
    app.exec();
    return 0;
}