# PC4 BRAZO ROBOTICO 
seguir la guia de instalacion 

https://docs.ros.org/en/kilted/Installation/Alternatives/Ubuntu-Development-Setup.html

## PRIMEROS COMANDOS
```bash 
# importante
esau@DESKTOP-A3RPEKP:~$ source /opt/ros/kilted/setup.sh
```
Obtenemos el script bash desde esa ruta y lo activamos (ejecutamos) , de modo que importamos las variables PATH, LD_LIBRARY_PATH, PYTHONPATH,ROS_DISTRO al shell (terminal) actual donde se ejecuta , luego las librerias y paquetes de ROS2 se ejecutaran correctamente en el terminal actual, hace estas entre otras exportaciones
```bash
export ROS_DISTRO=kilted
export PATH=/opt/ros/kilted/bin:$PATH
```

Se realiza una prueba rapida para ver el mecanismo piblisher - suscriptor 
```bash
ros2 run demo_nodes_cpp talker
[INFO] [1764453104.711036905] [talker]: Publishing: 'Hello World: 3030'
[INFO] [1764453109.265536838] [talker]: Publishing: 'Hello World: 3031'
....
ros2 run demo_nodes_py listener
[INFO] [1764453104.712581219] [listener]: I heard: [Hello World: 3030]
[INFO] [1764453109.266554404] [listener]: I heard: [Hello World: 3031]
```
### turtlesim
Seguir los pasos de instalacion
```bash
sudo apt install ros-kilted-turtlesim
# ros2 <verbo-principal> <subcomando> [argumentos] [opciones]
ros2 pkg executables turtlesim
```
A sabe **ros2** es el ejecutable principal , **pkg** es el comando de alto nivel(grupo de operaciones) para trabajar con paquetes equivalente a un **namespace** pues CLI esta organizado jerarquicamente 
```bash
ros2
 └── pkg
      ├── list
      ├── executables
      ├── prefix
      ├── xml
      └── create
# se obtiene la lista de funciones del modulo
turtlesim turtle_teleop_key
turtlesim turtlesim_node
...
```
en tanto que el subcomando **executable** y **turtlesim** indiacan la operacion y el argumento posicional(paquete). OSea ejecutamos el paquete turtlesim via ros2 pkg executable.<br>
Ahora 
```bash
# ros2 comando_principal paquete ejecutable
# llamamos a las funciones listadas antes
ros2 run turtlesim turtlesim_node
# en otro terminal
ros2 run turtlesim turtle_teleop_key
```
El primero crea el nodo donde se encuentra la tortuga y el otro manipula sus movimientos


Se esta trabajando en **wsl**, debido a que QT(la libreria que dibuja la ventana de turtlesim) espera que **/run/user/1000**  tenga permisos 0700 solo el usuario puede acceder, pero en wsl tenemos 0755 todos pueden leer/ejecutar, con **sudo chmod 700 /run/user/1000** remediamos eso.

Como bien indica el tutorial al ejecutar **ros2 run turtlesim turtle_teleop_key** en un nueva terminal se crea un nodo desde donde controlamos a la tortuga en el nodo ejecutado antes, con las flechas es posible hacer mover a la tortuga en la ventana QT
<p align="center">
    <img src="qt.png" width="60%">
</p>

### qrt
Se sigue luego las indicaciones para la instalacion de **rqt**, un framework grafico modular para manipular y visualizar los componentes del grafo ROS2(nodos,topicos,servicios,parametros,acciones,etc)<br>

Al ejecutar **rqt** tenemos una ventana para el manejo de las tortugas, pero cómo esta ventana  localiza los nodos de donde estan las tortuga ?<br>
Del siguiente modo : al ejecutar **rqt** este reconocera al nodo ejecutado via **ros2 run turtlesim turtlesim_node**, puesto que este ultimo se registra en el grado ROS2 anunciando su informacion correspondiente: 
```bash 
nodo : **/turtlesim**   yo publico: **/turtle1/pose** suscribo  : **/turtle1/cmd_vel** → tengo : **/reset/clear..** 
```
Este anuncio es manejado por DDS(descubrimiento automaticamente peer-to-peer) , luego rqt escucha el grafo ROS2  y ubica el nodo **turtlesim**, es cuando **rqt_graph** dibuja ese nodo. 

Ya se tiene la GUI luego  **Plugins / Services / Service caller** , ya en runnnig , para agregar una nueva seleccionamos **/spawn** en el menu desplegable al lado de **Service**.Le asignamos un nombre y posicion, finalmente presionamos el boton **call** 
Observar que la venta qt creado por **ros2 run turtlesim turtlesim_node**, ahora tenemos 2 tortugas

Probando los servicios , ahora modificamos algunos servicios,  otorgamos un pen **/turtle1/set_pen** asignando los valores a R=255 G =0 B=0, actualizamos la llamada **call** y el color del pen ahora es ROJO. 

Sin embargo nuestra **nueva_tortuga(el nombre que se asigne)** aun no puede moverse , necesitamos un segundo nodo para controlarlo.
```bash
# en una nueva terminal
ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=turtle2/cmd_vel
```
<p align="center">
    <img src="dos_tortugas.png" 
    width="60%">
</p>

Entonces desde la terminal donde se ejecutó **ros2 run turtlesim turtle_teleop_key** se manipula a la primera tortuga y desde el terminal donde ejecutamos **ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=tortuga_2/cmd_vel** controlamos a la segunda.

Pero como ? que pasó?
Detallemos, el ultimo comando ejecuta el nodo que lee el teclado **turtle_teleop_key** pero luego pasa los comandos(--ros-args --remap) a la tortuga_2 , el comando **turtle1/cmd_vel** ahora es cambiado a **turtle2/cmd_vel**(remapeo), esto ocurre en el sistema de nombres del grafo de ROS2,de modo que el nodo turtlesim , donde viven las dos instancias "tortugas" quedan diferenciadas.

Un breve resumen de los comandos
```bash
# se recomienda ejecutar la preparacion del entorno en todas las terminales, por las razones mecionadas
source /opt/ros/kilted/setup.sh
ros2 pkg executables turtlesim 
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turttle_teleop_key
qrt
# deshovar 
ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=tortuga_2/cmd_vel
```
Se datalla en forma grafica el sistema anterior
### nodos (nodes)
<p align="center">
    <img src="grafo_ros2.png"
    width="75%">
</p>

Para obtener informacion de algun nodo: **ros2 node info /my_turtle** , cambiar el nombre : **ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle**

### temas(topicos)
Los tópicos son los canales por donde fluyen los mensajes de un nodo a otro. Es un canal de flujo unidireccional si bien un nodo puede estar suscrito a muchos topicos , no puede enviar info en el sentido contrario. Para realizar eso se necesitaria otro topic
```bash
              Topic: /wheel/status
    Rueda (Publisher)  ------------------>  Control (Subscriber)

             Topic: /wheel/commands
 Control (Publisher)  ------------------>   Rueda (Subscriber)

```
<p align="center">
    <img src="topic.png"
    width="70%">
</p>

### rqt_graph
##### topicos
En la ventana rqt **Plugins/Introspection/Node graph** para visualizar de forma introspectiva los nodos ,temas y conexiones.
<p align="center">
    <img src="rqt_graph.png"
    width="60%">
</p>

Comandos para listas los temas(topics) , el tipo de tema , datos que publican 
```bash
ros2 topic list 
ros2 topic list -t
ros2 topic echo /turtle1/cmd_vel
```
El ultimo muestra los datos de la posicion de la primera tortuga.
Ademas **ros2 topic info /turtle1/cmd_vel** muestra los publisher y subscriptors que usan ese topico(canal de comunicacion)
```bash
ros2 topic list -t
ros2 interface show geometry_msgs/msg/Twist
```
**ros2 topic list -t** da una salida **geometry_msgs/msg/Twist** esto es que en el paquete **geometry_msgs** hay un **msg** llamado **Twist** ; otro comando util **ros2 interface show geometry_msgs/msg/Twist** para ver la estructura que espera el mensaje.

Para publicar datos en un tema directamente desde linea de comandos se usa 
```bash
ros2 topic pub <topic_name> <msg_type> '<args>'
# datos en formato YAML 
# publicamos ---- en canal----el tipo de mensaje----mensaje
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
#mensaje vacio
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" --rate 1
# autocompletar
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist <TAB>...
# una alternativa a YAML
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist \'linear:\^J\ \ x:\ 0.0\^J\ \ y:\ 0.0\^J\ \ z:\ 0.0\^Jangular:\^J\ \ x:\ 0.0\^J\ \ y:\ 0.0\^J\ \ z:\ 0.0\^J\'
```
Para que nuestro robot(en este caso la tortuga ) se mueva de manera constante se usaria el siguiente comando
```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
```
O para publicar solo una vez
```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
```
<p align="center">
    <img src="comandos.png"
    width ="70%">
</p>

Para ver las posiciones **ros2 topic echo /turtle1/pose** . O publicar mensajees con marca de tiempo **ros2 topic pub /pose geometry_msgs/msg/PoseStamped '{header: "auto", pose: {position: {x: 1.0, y: 2.0, z: 3.0}}}'**, y para observar info adicional:
```bash
# velocidad de mensajes
ros2 topic hz /turtle1/pose 
#ancho de banda usado
ros2 topic bw /turtle1/pose
#encontrar tpicos que usen el tipo de mensaje
ros2 topic find <topic_type>
```
##### servicios
Se podria profundizar mas, el tema es muy interesante, sin embargo ahora se realiza lo practico
