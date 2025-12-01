# COMO EJECUTAR
```bash
#entorno ROS2
source /opt/ros/kilted/setup.bash
#nuestro entorno
source ~/pc4_robotica/brazo_robot_ws/install/setup.bash
#construccion
 ros2 launch brazo_pkg brazo_sim.launch.py
## en RViz 
Displays/Global Options / Fixed Frame → escoger base_link
luego add RobotModel /Description Topic → "/robot_description" (nuestro brazo)
```
Y en otro terminal 
```bash
source /opt/ros/kilted/setup.bash
source ~/pc4_robotica/brazo_robot_ws/install/setup.bash
#enviar comandos para movimiento
python brazo_robot_ws/src/brazo_pkg/brazo_pkg/mover_brazo.py
# es posible que tenga que matar el proceso anterior y volver a ejecutar el comando, si la comunicacion crea "parpadeos"
```
