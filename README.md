ball_masterとball_detectorとball_operateの３つを使います。  
  
ros2 launch ball_master ball_system.launch.py  
でラウンチを実行する   

ball_detector_node   ← 視覚認識  
ball_operate_node    ← 追従・停止・後退制御  
ball_master_node     ← アクション管理（司令塔）  
