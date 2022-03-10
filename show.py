#!/usr/bin/env python3
"""
Pygame動作確認
# Pygame キーボード入力のイベント操作
https://shizenkarasuzon.hatenablog.com/entry/2019/02/08/184932
# Pygame イベントハンドラを使ってマウスイベントを作成
https://shizenkarasuzon.hatenablog.com/entry/2019/02/08/183005
"""
import sys
from PIL import Image, ImageDraw

import const
import maze


class ShowMap():
    """ 地図の表示 """
    
    # 1マスのサイズ（可変）
    size = 20
    
    def __init__(self):
        """ コンストラクタ """
        pass
    
    def draw_all(self, obj_maze):
        """ 地図全体を描画 """
        img = Image.new('RGB', (const.WIDTH, const.HEIGHT), color=0)
        self.draw = ImageDraw.Draw(img)
        # 壁の色
        COLOR_WALL = (255, 255, 255)
        # 扉の色
        COLOR_DOOR = (255, 127, 0)
        # 部屋の色
        COLOR_ROOM = (255, 255, 0)
        # イベント天井の色
        COLOR_CEILING = (0, 255, 0)
        # イベント床の色
        COLOR_FLOOR = (0, 0, 255)
        # 枠の描画
        self.draw.rectangle(
                (0, 0) + (const.WIDTH - 1, const.HEIGHT - 1), 
                outline=COLOR_WALL)
        # 迷路オブジェクトから各内容を取得
        maze_wall = obj_maze.maze_wall
        maze_door = obj_maze.maze_door
        maze_contents = obj_maze.maze_contents
        # 1マスのサイズの調整
        self.size = const.WIDTH // len(maze_wall[0])
        # 壁の大きさ
        wl = self.size * 0.95 / 2
        # イベントマークの大きさ
        ev = self.size * 0.8 / 2
        for iy, row_wall in enumerate(maze_wall):
            for ix, cell_wall in enumerate(row_wall):
                # 各セルの中心座標
                x = self.size * (ix + 0.5)
                y = self.size * (iy + 0.5)
                # 壁の描画
                if cell_wall & const.MAZE_NORTH != const.MAZE_NONE:
                    xy = (x - wl, y - wl) + (x + wl, y - wl)
                    self.draw.line(xy, fill=COLOR_WALL)
                if cell_wall & const.MAZE_SOUTH != const.MAZE_NONE:
                    xy = (x - wl, y + wl) + (x + wl, y + wl)
                    self.draw.line(xy, fill=COLOR_WALL)
                if cell_wall & const.MAZE_WEST != const.MAZE_NONE:
                    xy = (x - wl, y - wl) + (x - wl, y + wl)
                    self.draw.line(xy, fill=COLOR_WALL)
                if cell_wall & const.MAZE_EAST != const.MAZE_NONE:
                    xy = (x + wl, y - wl) + (x + wl, y + wl)
                    self.draw.line(xy, fill=COLOR_WALL)
                # 扉の描画
                cell_door = maze_door[iy][ix]
                if cell_door & const.MAZE_NORTH != const.MAZE_NONE:
                    xy = (x - wl, y - wl) + (x + wl, y - wl)
                    self.draw.line(xy, fill=COLOR_DOOR)
                if cell_door & const.MAZE_SOUTH != const.MAZE_NONE:
                    xy = (x - wl, y + wl) + (x + wl, y + wl)
                    self.draw.line(xy, fill=COLOR_DOOR)
                if cell_door & const.MAZE_WEST != const.MAZE_NONE:
                    xy = (x - wl, y - wl) + (x - wl, y + wl)
                    self.draw.line(xy, fill=COLOR_DOOR)
                if cell_door & const.MAZE_EAST != const.MAZE_NONE:
                    xy = (x + wl, y - wl) + (x + wl, y + wl)
                    self.draw.line(xy, fill=COLOR_DOOR)
                # イベント
                cell_contents = maze_contents[iy][ix]
                # イベント天井の描画
                if cell_contents & const.EVENT_CEILING != const.MAZE_NONE:
                    xy = (x, y - ev)
                    xy += (x - ev, y)
                    xy += (x + ev, y)
                    self.draw.polygon(xy, fill=COLOR_CEILING, outline=COLOR_CEILING)
                # イベント床の描画
                if cell_contents & const.EVENT_FLOOR != const.MAZE_NONE:
                    xy = (x, y + ev)
                    xy += (x - ev, y)
                    xy += (x + ev, y)
                    self.draw.polygon(xy, fill=COLOR_FLOOR, outline=COLOR_FLOOR)
                # 部屋の描画
                #if cell_contents & const.CONTENTS_ROOM != const.MAZE_NONE:
                #    xy = (x, y)
                #    self.draw.point(xy, COLOR_ROOM)
        return img
    
    def draw_player(self, px, py, direction):
        """ プレイヤーの位置表示 """
        # プレイヤーの色
        COLOR_PLAYER = (255, 0, 0)
        # 大きさ
        p = self.size * 0.7 / 2
        # 中心座標
        x = self.size * (px + 0.5)
        y = self.size * (py + 0.5)
        # 向き毎に描画
        if direction == const.DIR_NORTH:
            xy = (x, y - p) + (x - p, y + p) + (x + p, y + p)
        elif direction == const.DIR_SOUTH:
            xy = (x, y + p) + (x - p, y - p) + (x + p, y - p)
        elif direction == const.DIR_EAST:
            xy = (x + p, y) + (x - p, y - p) + (x - p, y + p)
        elif direction == const.DIR_WEST:
            xy = (x - p, y) + (x + p, y - p) + (x + p, y + p)
        self.draw.polygon(xy, fill=COLOR_PLAYER, outline=COLOR_PLAYER)
