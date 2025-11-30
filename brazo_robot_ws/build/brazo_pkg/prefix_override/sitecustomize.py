import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/esau/pc4_robotica/brazo_robot_ws/install/brazo_pkg'
