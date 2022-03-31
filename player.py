#!/usr/bin/env python3
"""
プレイヤー
"""
import sys
from PIL import Image, ImageDraw

import const


class Player:
    """ プレイヤークラス """
    name = ''
    floor = 1
    x = 0
    y = 0
    direction = const.DIR_SOUTH
    
    # オートマッピング用（階層ごとに配列で用意）
    mapping = None
    
    def __init__(self, name, obj_maze=None):
        """ コンストラクタ """
        self.name = name
        if obj_maze is not None:
            map_floor = []
            for j in range(obj_maze.height):
                row = []
                for i in range(obj_maze.width):
                    row.append(False)
                map_floor.append(row)
            self.mapping = [map_floor]
    
    def auto_mapping(self):
        """ オートマッピング """
        # 次の階層
        if len(self.mapping) < self.floor:
            map_floor = []
            for j in range(len(self.mapping[0])):
                row = []
                for i in range(len(self.mapping[0][0])):
                    row.append(False)
                map_floor.append(row)
            self.mapping.append(map_floor)
        # 通った場所に印を付ける
        self.mapping[self.floor - 1][self.y][self.x] = True
    
    def move_forward(self, cell_wall):
        """ 前方へ移動 """
        # ※外枠判定はこのメソッド外で処理すること
        if self.direction == const.DIR_NORTH:
            if cell_wall & const.MAZE_NORTH == const.MAZE_NONE:
                self.y -= 1
        elif self.direction == const.DIR_SOUTH:
            if cell_wall & const.MAZE_SOUTH == const.MAZE_NONE:
                self.y += 1
        elif self.direction == const.DIR_WEST:
            if cell_wall & const.MAZE_WEST == const.MAZE_NONE:
                self.x -= 1
        elif self.direction == const.DIR_EAST:
            if cell_wall & const.MAZE_EAST == const.MAZE_NONE:
                self.x += 1
    
    def turn_left(self):
        """ 左に向く """
        if self.direction == const.DIR_NORTH:
            self.direction = const.DIR_WEST
        elif self.direction == const.DIR_EAST:
            self.direction = const.DIR_NORTH
        elif self.direction == const.DIR_SOUTH:
            self.direction = const.DIR_EAST
        elif self.direction == const.DIR_WEST:
            self.direction = const.DIR_SOUTH
    
    def turn_right(self):
        """ 右に向く """
        if self.direction == const.DIR_NORTH:
            self.direction = const.DIR_EAST
        elif self.direction == const.DIR_EAST:
            self.direction = const.DIR_SOUTH
        elif self.direction == const.DIR_SOUTH:
            self.direction = const.DIR_WEST
        elif self.direction == const.DIR_WEST:
            self.direction = const.DIR_NORTH
    
    def turn_around(self):
        """ 振り向く """
        if self.direction == const.DIR_NORTH:
            self.direction = const.DIR_SOUTH
        elif self.direction == const.DIR_EAST:
            self.direction = const.DIR_WEST
        elif self.direction == const.DIR_SOUTH:
            self.direction = const.DIR_NORTH
        elif self.direction == const.DIR_WEST:
            self.direction = const.DIR_EAST
