#!/usr/bin/env python3
"""
Pygame動作確認
# Pygame キーボード入力のイベント操作
https://shizenkarasuzon.hatenablog.com/entry/2019/02/08/184932
# Pygame イベントハンドラを使ってマウスイベントを作成
https://shizenkarasuzon.hatenablog.com/entry/2019/02/08/183005
"""
from pygame.locals import *
import pygame
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
        draw = ImageDraw.Draw(img)
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
        draw.rectangle(
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
                    draw.line(xy, fill=COLOR_WALL)
                if cell_wall & const.MAZE_SOUTH != const.MAZE_NONE:
                    xy = (x - wl, y + wl) + (x + wl, y + wl)
                    draw.line(xy, fill=COLOR_WALL)
                if cell_wall & const.MAZE_WEST != const.MAZE_NONE:
                    xy = (x - wl, y - wl) + (x - wl, y + wl)
                    draw.line(xy, fill=COLOR_WALL)
                if cell_wall & const.MAZE_EAST != const.MAZE_NONE:
                    xy = (x + wl, y - wl) + (x + wl, y + wl)
                    draw.line(xy, fill=COLOR_WALL)
                # 扉の描画
                cell_door = maze_door[iy][ix]
                if cell_door & const.MAZE_NORTH != const.MAZE_NONE:
                    xy = (x - wl, y - wl) + (x + wl, y - wl)
                    draw.line(xy, fill=COLOR_DOOR)
                if cell_door & const.MAZE_SOUTH != const.MAZE_NONE:
                    xy = (x - wl, y + wl) + (x + wl, y + wl)
                    draw.line(xy, fill=COLOR_DOOR)
                if cell_door & const.MAZE_WEST != const.MAZE_NONE:
                    xy = (x - wl, y - wl) + (x - wl, y + wl)
                    draw.line(xy, fill=COLOR_DOOR)
                if cell_door & const.MAZE_EAST != const.MAZE_NONE:
                    xy = (x + wl, y - wl) + (x + wl, y + wl)
                    draw.line(xy, fill=COLOR_DOOR)
                # イベント
                cell_contents = maze_contents[iy][ix]
                # イベント天井の描画
                if cell_contents & const.EVENT_CEILING != const.MAZE_NONE:
                    xy = (x, y - ev)
                    xy += (x - ev, y)
                    xy += (x + ev, y)
                    draw.polygon(xy, fill=COLOR_CEILING, outline=COLOR_CEILING)
                # イベント床の描画
                if cell_contents & const.EVENT_FLOOR != const.MAZE_NONE:
                    xy = (x, y + ev)
                    xy += (x - ev, y)
                    xy += (x + ev, y)
                    draw.polygon(xy, fill=COLOR_FLOOR, outline=COLOR_FLOOR)
                # 部屋の描画
                #if cell_contents & const.CONTENTS_ROOM != const.MAZE_NONE:
                #    xy = (x, y)
                #    draw.point(xy, COLOR_ROOM)
        return img, draw
    
    def draw_player(self, draw, px, py, direction):
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
        draw.polygon(xy, fill=COLOR_PLAYER, outline=COLOR_PLAYER)


if __name__ == '__main__':
    # テストコード
    import time
    #seed = time.time_ns() % (10 ** 9)
    seed = 123
    #seed = 79457659
    print('random.seed = ' + str(seed))
    obj_maze = maze.Maze(100, 100, seed=seed, room=100)
    #obj_maze = maze.Maze(20, 20, seed=seed, room=50)
    obj_maze.make_maze()
    
    ### 表示
    # Pygameを初期化
    pygame.init()
    # 画面を作成
    screen = pygame.display.set_mode((const.WIN_W, const.WIN_H))
    # タイトルを作成
    pygame.display.set_caption('Maze')
    # 時間オブジェクト生成
    clock = pygame.time.Clock()
    
    # 描画
    showmap = ShowMap()
    img, draw = showmap.draw_all(obj_maze)
    #showmap.draw_player(draw, 6, 3, const.DIR_SOUTH)
    showmap.draw_player(draw, 11, 4, const.DIR_EAST)
    
    myImage = pygame.image.frombuffer(img.tobytes(), img.size, img.mode)
    # 余白
    margin = (const.WIN_W - const.WIDTH) // 2
    
    while True:
        # フレームレート設定
        clock.tick(10)
        # 描画
        screen.fill((0, 0, 0))
        screen.blit(myImage, (margin, margin))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # キーを押したとき
            if event.type == KEYDOWN:
                # ESCキーならスクリプトを終了
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    print("押されたキー = " + pygame.key.name(event.key))
            # マウスクリック時の動作
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                print('mouse clicked -> (' + str(x) + ', ' + str(y) + ')', end=', ')
                print("Button Number = " + str(event.button))
            # マウスポインタが移動したときの動作
            if event.type == MOUSEMOTION:
                x, y = event.pos
                #print("mouse moved   -> (" + str(x) + ", " + str(y) + ")")
            pygame.display.update()

