#!/usr/bin/env python3
"""
Pygame動作確認
"""
import sys
import pygame
from pygame.locals import *
from PIL import Image, ImageDraw

import const


class Player:
    """ プレイヤークラス """
    name = ''
    x = 0
    y = 0
    direction = const.DIR_SOUTH
    
    def __init__(self, name):
        """ コンストラクタ """
        self.name = name
    
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
    


# テストコード
def test_main():
    """ テスト用メイン関数 """
    # Pygameを初期化
    pygame.init()
    # 画面を作成
    screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    # タイトルを作成
    pygame.display.set_caption('test')
    
    # 時間オブジェクト生成
    clock = pygame.time.Clock()
    
    # PILで描画
    pilImage = Image.new('RGB', (20, 20), color=0)
    draw = ImageDraw.Draw(pilImage)
    xy = (0, 19) + (9, 0) + (19, 19)
    draw.polygon(xy, fill=(255,0,0), outline=(255,255,0))
    #myImage = pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode)
    myImage = pygame.image.frombuffer(pilImage.tobytes(), pilImage.size, pilImage.mode)
    
    # プレイヤーの初期設定
    p = Player('tester')
    p.x = 230
    p.y = 300
    p.direction = const.DIR_NORTH
    
    cell_wall = const.MAZE_NONE
    
    # ループ
    while True:
        # フレームレート設定
        clock.tick(15)
        # 背景色設定
        screen.fill((0, 0, 0))
        
        screen.blit(myImage, (p.x, p.y))
        # イベント処理
        for event in pygame.event.get():
            # 終了処理
            if event.type == QUIT:
                end()
            # キーを押したとき
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # ESCキーならスクリプトを終了
                    end()
                elif event.key == K_UP:
                    p.move_forward(cell_wall)
                    print(str(p.x) + ',' + str(p.y))
                elif event.key == K_LEFT:
                    p.turn_left()
                elif event.key == K_RIGHT:
                    p.turn_right()
                elif event.key == K_DOWN:
                    p.turn_around()
                else:
                    print("押されたキー = " + pygame.key.name(event.key))
                    #screen.blit(myImage, (0, 50))
                # 向きにより画像を変更
                if p.direction == const.DIR_NORTH:
                    xy = (0, 19) + (9, 0) + (19, 19)
                elif p.direction == const.DIR_SOUTH:
                    xy = (0, 0) + (19, 0) + (9, 19)
                elif p.direction == const.DIR_EAST:
                    xy = (0, 0) + (0, 19) + (19, 9)
                elif p.direction == const.DIR_WEST:
                    xy = (0, 9) + (19, 0) + (19, 19)
                pilImage = Image.new('RGB', (20, 20), color=0)
                draw = ImageDraw.Draw(pilImage)
                draw.polygon(xy, fill=(255,0,0), outline=(255,255,0))
                myImage = pygame.image.frombuffer(pilImage.tobytes(), pilImage.size, pilImage.mode)
                screen.fill((0, 0, 0))
                screen.blit(myImage, (p.x, p.y))
            # マウスクリック時の動作
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                print('mouse clicked -> (' + str(x) + ', ' + str(y) + ')', end=', ')
                print("Button Number = " + str(event.button))
            # マウスポインタが移動したときの動作
            if event.type == MOUSEMOTION:
                x, y = event.pos
                #print("mouse moved   -> (" + str(x) + ", " + str(y) + ")")
            # 画面更新
            pygame.display.update()


def end():
    """ 終了関数 """
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    test_main()
