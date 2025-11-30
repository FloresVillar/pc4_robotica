from setuptools import setup
import os
from glob import glob

package_name = 'brazo_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Esau',
    maintainer_email='tu_email@dominio.com',
    description='Paquete de ejemplo para controlar un brazo robot en ROS 2 Kilted',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'mover_brazo = brazo_pkg.mover_brazo:main',
        ],
    },
    data_files=[
        # Esto asegura que package.xml se instale correctamente
        ('share/{}'.format(package_name), ['package.xml']),
        ('share/{}/launch'.format(package_name), glob('launch/*.launch.py')),
        ('share/{}/rviz'.format(package_name), glob('rviz/*.rviz')),
        ('share/{}/urdf'.format(package_name), glob('urdf/*.xacro')),
        # si tienes meshes
        ('share/{}/meshes'.format(package_name), glob('meshes/*')),
    ],
)
