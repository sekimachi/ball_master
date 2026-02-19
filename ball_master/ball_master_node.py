from rclpy.node import Node
from rclpy.action import ActionServer
from imrc_messages.action import BallColor
import rclpy
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Bool



class BallMaster(Node):

    def __init__(self):
        super().__init__('ball_master')
        self.get_logger().info('Ball Master Node 起動しました')

    
        self.state = "IDLE"
        self.target_color = None
        self.ball_catch = False
        self.detect_failed = False
            

        # ===== 色指令用 Publisher =====
        self.color_pub = self.create_publisher(String,'detect_ball_color',10)

        # ===== Publisher =====
        self.operate_enable_pub = self.create_publisher(Bool, 'ball_operate_enable', 10)

        # ===== Action Server =====
        self._action_server = ActionServer( self,BallColor,'ball_color',self.execute_callback)
        
        # ===== Subscriber =====
        self.create_subscription(Bool, 'detect_ball_status', self.status_cb, 10)
        self.create_subscription(Bool, 'ball_capture', self.capture_cb, 10)

        
    # =================================================================
    # action のコールバック関数。Action が呼び出されたときに実行される。
    # =================================================================
    def execute_callback(self, goal_handle):
        self.get_logger().info("Actionを受け取ったよ！")

        # ==== 初期化 ====
        self.target_color = goal_handle.request.color
        self.state = "SEARCHING"
        self.ball_catch = False
        self.ball_catch = False
        self.detect_failed = False

        # === publish ==== 
        msg = Bool()
        msg.data = True
        self.operate_enable_pub.publish(msg)
        self.get_logger().info(f"ball_operate_enable にパブリッシュ: {msg.data}")

        msg = String()
        msg.data = self.target_color
        self.color_pub.publish(msg)
        self.get_logger().info(f"detect_ball_color にパブリッシュ: {self.target_color}")
        feedback = BallColor.Feedback()


        # ==== 実行ループ ====
        while rclpy.ok():
            feedback.state = self.state
            goal_handle.publish_feedback(feedback)

            if self.ball_catch:
                self.state = "IDLE"
                msg = Bool()
                msg.data = False
                self.operate_enable_pub.publish(msg)
                goal_handle.succeed()
                self.ball_catch = False
                return BallColor.Result(success=True)
            
            if self.detect_failed:
                msg = Bool()
                msg.data = False
                self.operate_enable_pub.publish(msg)
                goal_handle.abort()
                self.detect_failed = False
                return BallColor.Result(success=False)

            rclpy.spin_once(self, timeout_sec=0.1)
        # ====================

    # ===============================
    # ball_captureのコールバック。ball_operateノードから捕獲成功の通知を受け取る。
    # ===============================
    def capture_cb(self, msg: Bool):
        if msg.data:
            self.get_logger().info("operate_nodeから捕獲成功の通知を受信")
            self.ball_catch = True
            self.state = "CAPTURED"

    def status_cb(self, msg):
        if not msg.data:
            self.get_logger().error("Detector_nodeで失敗通知を受信")
            self.state = "IDLE"
            self.ball_catch = False
            self.detect_failed = True


def main():
    rclpy.init()
    node = BallMaster()
    rclpy.spin(node)
    rclpy.shutdown()