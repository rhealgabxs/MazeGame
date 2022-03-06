"""
定数
"""

# 迷路の内容
#   0b0000  北:道、東:道、南:道、西:道
#   0b1000  北:壁、東:道、南:道、西:道
#   0b0100  北:道、東:壁、南:道、西:道
#   0b0010  北:道、東:道、南:壁、西:道
#   0b0001  北:道、東:道、南:道、西:壁
MAZE_NONE = 0b0000
MAZE_NORTH = 0b0001
MAZE_EAST = 0b0010
MAZE_SOUTH = 0b0100
MAZE_WEST = 0b1000
MAZE_ALL = MAZE_NORTH | MAZE_EAST | MAZE_SOUTH | MAZE_WEST
CONTENTS_ROOM = 1
EVENT_FLOOR = 0b0001_0000_0000
EVENT_CEILING = 0b0010_0000_0000
EVENT_BOTH = EVENT_CEILING | EVENT_FLOOR

# 方角
DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3

# 視界範囲
VIEW = 5

# ウィンドウのサイズ
WIN_W = 600
WIN_H = 600
# 描画範囲
WIDTH = 500
HEIGHT = 500
# 壁の基本の大きさ
WALL = 100
# 視野角（1〜180）
#ANGLE = 60
# 視点からの距離、視野 (field of view)
#FOV = 1 / math.tan(ANGLE * 0.5 * math.pi / 180)
#FOV = 2     # 視野角 : 53.130deg
FOV = 1.5   # 視野角 : 67.380deg

