from setuptools import find_packages, setup

package_name = 'python_service'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/'+package_name+'/resource',['resource/face.jpg','resource/test.jpg'])
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
            "python_server = python_service.face_detect:main",
            "face_node = python_service.face_node:main",
            "face_cilent_node = python_service.face_cilent_node:main"
        ],
    },
)
