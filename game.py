#!/usr/bin/env python3
"""
Pygame動作確認
"""
import random
import sys
import time
import pygame
from pygame.locals import *
from PIL import Image, ImageDraw

import const
import draw
import maze
import player
import show


def main():
    """ メイン関数 """
    
    # Pygameを初期化
    pygame.init()
    # 画面を作成
    screen = pygame.display.set_mode((const.WIN_W, const.WIN_H))
    # タイトルを作成
    pygame.display.set_caption('Maze')
    # 時間オブジェクト生成
    clock = pygame.time.Clock()
    
    # 迷路作成
    seed = time.time_ns() % (10 ** 9)
    #seed = 123
    print('random.seed = ' + str(seed))
    mz = maze.Maze(20, 20, seed=seed, room=50)
    mz.make_maze()
    
    # プレイヤー作成
    pl = player.Player('Player')
    # スタート位置決定
    pl.x = mz.x_up
    pl.y = mz.y_up
    pl.direction = random.choice(
            [const.DIR_NORTH, const.DIR_EAST, const.DIR_WEST, const.DIR_SOUTH])
    
    # 3D描画
    draw3d = draw.Draw3D()
    # プレイヤーが歩いた場所の初期化
    maze_mark = [[0 for i in range(len(mz.maze_wall[0]))]
                    for j in range(len(mz.maze_wall))]
    #maze_mark[pl.y][pl.x] = 1
    ### TODO: 歩いた場所のみ地図表示
    
    # 地図描画
    showmap = show.ShowMap()
    
    # 画面背景色
    COLOR_BACK = (0, 0, 0)
    # 画面と描画領域の余白
    margin = (const.WIN_W - const.WIDTH) // 2
    
    screen.fill(COLOR_BACK)
    # ループ
    while True:
        # フレームレート設定
        clock.tick(15)
        # 描画
        img3d = draw3d.draw(mz, pl.x, pl.y, pl.direction)
        img = pygame.image.frombuffer(img3d.tobytes(), img3d.size, img3d.mode)
        screen.blit(img, (margin, margin))
        # イベント処理
        for event in pygame.event.get():
            # 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # キー入力判定
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # ESCキーなら終了
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP:
                    cell_wall = mz.maze_wall[pl.y][pl.x]
                    pl.move_forward(cell_wall)
                elif event.key == K_LEFT:
                    pl.turn_left()
                elif event.key == K_RIGHT:
                    pl.turn_right()
                elif event.key == K_DOWN:
                    pl.turn_around()
                elif event.key == K_m:
                    # 地図表示
                    imgmap, drawmap = showmap.draw_all(mz)
                    showmap.draw_player(drawmap, pl.x, pl.y, pl.direction)
                    screen.fill(COLOR_BACK)
                    img = pygame.image.frombuffer(
                            imgmap.tobytes(), imgmap.size, imgmap.mode)
                    screen.blit(img, (margin, margin))
                else:
                    pass
            # 画面更新
            pygame.display.update()


if __name__ == "__main__":
    # 処理開始
    main()
