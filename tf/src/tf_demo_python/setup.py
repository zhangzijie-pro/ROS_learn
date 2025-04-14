from setuptools import find_packages, setup

package_name = 'tf_demo_python'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zzj',
    maintainer_email='zzj@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "tf_publish=tf_demo_python.static_tf_broadcaster:main",
            "dynamic_tf_publish=tf_demo_python.dynamic_tf_broadcaster:main",
            "tf_listener=tf_demo_python.tf_listener:main",
        ],
    },
)
