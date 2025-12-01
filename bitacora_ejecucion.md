# COMO EJECUTAR
```bash
#entorno ROS2
source /opt/ros/kilted/setup.bash
#nuestro entorno
source ~/pc4_robotica/brazo_robot_ws/install/setup.bash
#construccion
 ros2 launch brazo_pkg brazo_sim.launch.py
```
Y en otro terminal 
```bash
#enviar comandos para movimiento
python brazo_robot_ws/src/brazo_pkg/brazo_pkg/mover_brazo.py
```
