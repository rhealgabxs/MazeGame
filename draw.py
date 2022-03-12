#!/usr/bin/env python3
"""
3次元描画
"""
import sys
from PIL import Image, ImageDraw

import const


class Draw3D:
    """ 3次元描画クラス """
    
    # 地図の参照順序
    #   左端→左側→右端→右側→真ん中 の順
    MAP_ORDER = list(range(const.VIEW)) \
            + [i for i in range(const.VIEW * 2, const.VIEW - 1, -1)]
    
    def __init__(self):
        """ コンストラクタ """
        pass
    
    def draw(self, obj_maze, x, y, direction):
        """
        描画メソッド
        引数：
            obj_maze : 迷路オブジェクト
            x, y : プレイヤーの位置
            direction : プレイヤーの向き
        """
        # 描画の初期化
        img = Image.new('RGB', (const.WIDTH, const.HEIGHT), color=0)
        draw = ImageDraw.Draw(img)
        # 床、天井の描画
        self.draw_updown(draw)
        # 可視範囲の地図情報取得
        map_view = self.get_map_visible(obj_maze, x, y, direction)
        # 壁の描画
        self.draw_wall(draw, map_view, direction)
        # 枠の描画
        draw.rectangle(
                (0, 0) + (const.WIDTH - 1, const.HEIGHT - 1),
                outline=(255, 255, 255))
        # 戻り値
        return img
    
    def get_map_visible(self, obj_maze, x, y, direction):
        """
        可視範囲の地図情報取得
            「手前→奥」「左→右」で取得
            範囲外は反対側の場所
        """
        maze_wall = obj_maze.maze_wall
        maze_door = obj_maze.maze_door
        maze_contents = obj_maze.maze_contents
        # 可視範囲の情報
        view_wall = []
        view_door = []
        view_contents = []
        # 見た方向の地図情報を取得
        depth_range = None
        depth_mod_b = None
        lr_range = None
        lr_mod_b = None
        if direction == const.DIR_EAST:
            # 東
            depth_range = range(x, x + const.VIEW + 1)
            lr_range = range(y - const.VIEW, y + const.VIEW + 1)
        elif direction == const.DIR_WEST:
            # 西
            depth_range = range(x, x - const.VIEW - 1, -1)
            lr_range = range(y + const.VIEW, y - const.VIEW - 1, -1)
        elif direction == const.DIR_SOUTH:
            # 南
            depth_range = range(y, y + const.VIEW + 1)
            lr_range = range(x + const.VIEW, x - const.VIEW - 1, -1)
        elif direction == const.DIR_NORTH:
            # 北
            depth_range = range(y, y - const.VIEW - 1, -1)
            lr_range = range(x - const.VIEW, x + const.VIEW + 1)
        # 情報取得
        for depth in depth_range:
            row_wall = []
            row_door = []
            row_contents = []
            for lr in lr_range:
                i = 0
                j = 0
                if (direction == const.DIR_NORTH 
                        or direction == const.DIR_SOUTH):
                    i = lr % len(maze_wall[0])
                    j = depth % len(maze_wall)
                elif (direction == const.DIR_EAST 
                        or direction == const.DIR_WEST):
                    i = depth % len(maze_wall[0])
                    j = lr % len(maze_wall)
                row_wall.append(maze_wall[j][i])
                row_door.append(maze_door[j][i])
                row_contents.append(maze_contents[j][i])
            view_wall.append(row_wall)
            view_door.append(row_door)
            view_contents.append(row_contents)
        # 戻り値
        map_view = [view_wall, view_door, view_contents]
        return map_view
    
    def draw_wall(self, draw, map_view, direction):
        """ 壁の描画 """
        view_wall, view_door, view_contents = map_view
        # 壁の色
        COLOR_WALL = (255, 255, 255)
        # 扉の色
        COLOR_DOOR = (255, 255, 255)
        # イベントの色
        COLOR_EVENT = (255, 255, 255)
        # 壁の有無により描画
        for depth in range(const.VIEW, -1, -1):
            for i in self.MAP_ORDER:
                # 3Dの場所（視点（中心）からの距離）
                d3_x_left = (i - const.VIEW) * 2 - 1
                d3_x_right = (i - const.VIEW) * 2 + 1
                d3_y = 1
                d3_z = depth + 1
                d3_z_here = depth
                # イベント床の描画
                if view_contents[depth][i] & const.EVENT_FLOOR > 0:
                    d2_x, d2_y = self.transform(d3_x_left + 0.3, d3_y, d3_z_here + 0.15)
                    xy = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    d2_x, d2_y = self.transform(d3_x_left + 0.3, d3_y, d3_z - 0.15)
                    xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    d2_x, d2_y = self.transform(d3_x_right - 0.3, d3_y, d3_z - 0.15)
                    xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    d2_x, d2_y = self.transform(d3_x_right - 0.3, d3_y, d3_z_here + 0.15)
                    xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    draw.polygon(xy, fill=COLOR_EVENT, outline=COLOR_EVENT)
                # イベント天井の描画
                if view_contents[depth][i] & const.EVENT_CEILING > 0:
                    d2_x, d2_y = self.transform(d3_x_left + 0.3, d3_y, d3_z_here + 0.15)
                    xy = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    d2_x, d2_y = self.transform(d3_x_left + 0.3, d3_y, d3_z - 0.15)
                    xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    d2_x, d2_y = self.transform(d3_x_right - 0.3, d3_y, d3_z - 0.15)
                    xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    d2_x, d2_y = self.transform(d3_x_right - 0.3, d3_y, d3_z_here + 0.15)
                    xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    draw.polygon(xy, fill=COLOR_EVENT, outline=COLOR_EVENT)
                # 前面の壁＆扉の描画
                cell_judge = const.MAZE_NORTH << direction
                if (view_wall[depth][i] & cell_judge > 0
                        or view_door[depth][i] & cell_judge > 0):
                    d2_x_left, d2_y_left = self.transform(d3_x_left, d3_y, d3_z)
                    d2_x_right, d2_y_right = self.transform(d3_x_right, d3_y, d3_z)
                    xy = self.xy_wall(
                            d2_x_left, d2_y_left, 
                            d2_x_right, d2_y_right)
                    draw.polygon(xy, fill=0, outline=COLOR_WALL)
                if view_door[depth][i] & cell_judge > 0:
                    d2_x, d2_y = self.transform(d3_x_left + 0.4, d3_y, d3_z)
                    xy = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    d2_x, d2_y = self.transform(d3_x_left + 0.4, d3_y - 0.4, d3_z)
                    xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    d2_x, d2_y = self.transform(d3_x_right - 0.4, d3_y - 0.4, d3_z)
                    xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    d2_x, d2_y = self.transform(d3_x_right - 0.4, d3_y, d3_z)
                    xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    draw.polygon(xy, outline=COLOR_DOOR)
                # 左の壁＆扉の描画
                cell_judge = const.MAZE_NORTH << ((direction - 1) % 4)
                if i <= const.VIEW \
                        and (view_wall[depth][i] & cell_judge > 0
                            or view_door[depth][i] & cell_judge > 0):
                    d2_x_left, d2_y_left = self.transform(d3_x_left, d3_y, d3_z_here)
                    d2_x_right, d2_y_right = self.transform(d3_x_left, d3_y, d3_z)
                    xy = self.xy_wall(
                            d2_x_left, d2_y_left, 
                            d2_x_right, d2_y_right)
                    draw.polygon(xy, fill=0, outline=COLOR_WALL)
                if view_door[depth][i] & cell_judge > 0:
                    d2_x, d2_y = self.transform(d3_x_left, d3_y, d3_z_here + 0.2)
                    xy1 = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    d2_x, d2_y = self.transform(d3_x_left, d3_y - 0.4, d3_z_here + 0.2)
                    xy2 = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    d2_x, d2_y = self.transform(d3_x_left, d3_y - 0.4, d3_z - 0.2)
                    xy3 = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    d2_x, d2_y = self.transform(d3_x_left, d3_y, d3_z - 0.2)
                    xy4 = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    draw.line(xy1 + xy2, fill=COLOR_DOOR)
                    draw.line(xy2 + xy3, fill=COLOR_DOOR)
                    draw.line(xy3 + xy4, fill=COLOR_DOOR)
                # 右の壁＆扉の描画
                cell_judge = const.MAZE_NORTH << ((direction + 1) % 4)
                if i >= const.VIEW \
                        and (view_wall[depth][i] & cell_judge > 0
                            or view_door[depth][i] & cell_judge > 0):
                    d2_x_left, d2_y_left = self.transform(d3_x_right, d3_y, d3_z)
                    d2_x_right, d2_y_right = self.transform(d3_x_right, d3_y, d3_z_here)
                    xy = self.xy_wall(
                            d2_x_left, d2_y_left, 
                            d2_x_right, d2_y_right)
                    draw.polygon(xy, fill=0, outline=COLOR_WALL)
                if view_door[depth][i] & cell_judge > 0:
                    d2_x, d2_y = self.transform(d3_x_right, d3_y, d3_z_here + 0.2)
                    xy1 = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    d2_x, d2_y = self.transform(d3_x_right, d3_y - 0.4, d3_z_here + 0.2)
                    xy2 = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    d2_x, d2_y = self.transform(d3_x_right, d3_y - 0.4, d3_z - 0.2)
                    xy3 = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                    d2_x, d2_y = self.transform(d3_x_right, d3_y, d3_z - 0.2)
                    xy4 = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                    draw.line(xy1 + xy2, fill=COLOR_DOOR)
                    draw.line(xy2 + xy3, fill=COLOR_DOOR)
                    draw.line(xy3 + xy4, fill=COLOR_DOOR)
    
    def draw_updown(self, draw):
        """ 床、天井の描画 """
        BORDER_COLOR = (255, 255, 255)
        for depth in range(0, const.VIEW + 1):
            for i in range(- const.VIEW, const.VIEW + 1):
                # 3Dの場所（視点（中心）からの距離）
                d3_x_left = i * 2 - 1
                d3_x_right = i * 2 + 1
                d3_y = 1
                d3_z = depth + 1
                d3_z_here = depth
                # 床
                d2_x, d2_y = self.transform(d3_x_left, d3_y, d3_z_here)
                xy = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                d2_x, d2_y = self.transform(d3_x_left, d3_y, d3_z)
                xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                d2_x, d2_y = self.transform(d3_x_right, d3_y, d3_z)
                xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                d2_x, d2_y = self.transform(d3_x_right, d3_y, d3_z_here)
                xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 + d2_y)
                draw.polygon(xy, outline=BORDER_COLOR)
                # 天井
                d2_x, d2_y = self.transform(d3_x_left, d3_y, d3_z_here)
                xy = (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                d2_x, d2_y = self.transform(d3_x_left, d3_y, d3_z)
                xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                d2_x, d2_y = self.transform(d3_x_right, d3_y, d3_z)
                xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                d2_x, d2_y = self.transform(d3_x_right, d3_y, d3_z_here)
                xy += (const.WIDTH / 2 + d2_x, const.HEIGHT / 2 - d2_y)
                draw.polygon(xy, outline=BORDER_COLOR)
    
    def transform(self, d3_x, d3_y, d3_z):
        """ 透視投影変換 """
        # 3D座標から2D座標に変換
        if d3_z == 0:
            # 計算後、描画枠からはみ出るような値
            d3_z = 0.1
        d2_x = d3_x / d3_z * const.FOV * const.WALL
        d2_y = d3_y / d3_z * const.FOV * const.WALL
        return d2_x, d2_y
    
    def xy_wall(self, d2_x_left, d2_y_left, d2_x_right, d2_y_right):
        """ 壁の描画座標を算出 """
        # 各座標を指定
        # 左下
        xy = (const.WIDTH / 2 + d2_x_left, const.HEIGHT / 2 + d2_y_left)
        # 左上
        xy += (const.WIDTH / 2 + d2_x_left, const.HEIGHT / 2 - d2_y_left)
        # 右上
        xy += (const.WIDTH / 2 + d2_x_right, const.HEIGHT / 2 - d2_y_right)
        # 右下
        xy += (const.WIDTH / 2 + d2_x_right, const.HEIGHT / 2 + d2_y_right)
        return xy
