#!/usr/bin/env python3
"""
迷路ゲーム本体
"""
import random
import sys
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

import const
import draw
import maze
import player
import search_maze
import show_map


class Game():
    """ ゲームクラス """
    # ウィンドウタイトル
    TITLE = 'Maze'
    
    # キーカウンタ
    count_key = 0
    # 歩数
    count_steps = 0
    # オートマッピングを開いた回数
    count_mapping = 0
    # 全体地図を開いた回数
    count_show_map = 0
    # 上り階段探索を開いた回数
    count_guide_up = 0
    # 下り階段探索を開いた回数
    count_guide_down = 0
    
    def __init__(self):
        """ コンストラクタ """
        # 画面と描画領域の余白
        self.margin = (const.WIN_W - const.WIDTH) // 2
        
        self.root = tk.Tk()
        self.root.title(self.TITLE)
        self.root.geometry(str(const.WIN_W) + 'x' + str(const.WIN_H))
        self.root.configure(bg='black')
        self.bind_id = self.root.bind('<KeyPress>', self.key_press)
        self.root.bind('<KeyPress-Shift_L>', self.key_press_shift)
        self.root.bind('<KeyPress-Shift_R>', self.key_press_shift)
        self.root.bind('<KeyRelease-Shift_L>', self.key_release_shift)
        self.root.bind('<KeyRelease-Shift_R>', self.key_release_shift)
        self.time_key = 0
        self.key_shift = False
        
        # 迷路作成
        self.seed = time.time_ns() % (10 ** 9)
        #self.seed = 123
        #print('random.seed = ' + str(self.seed))
        #self.mz = maze.Maze(100, 100, seed=self.seed, room=100)
        self.mz = maze.Maze(20, 20, seed=self.seed)
        self.mz.make_maze()
        
        # プレイヤー作成
        self.pl = player.Player('Player', self.mz)
        # スタート位置決定
        self.pl.x = self.mz.x_up
        self.pl.y = self.mz.y_up
        self.pl.direction = random.choice(
                [const.DIR_NORTH, const.DIR_EAST, 
                 const.DIR_SOUTH, const.DIR_WEST])
        # オートマッピング
        self.pl.auto_mapping()
        
        # 3D描画オブジェクト
        self.draw3d = draw.Draw3D()
        img3d = self.draw3d.draw(
                self.mz, self.pl.x, self.pl.y, self.pl.direction)
        
        # 地図描画オブジェクト
        self.obj_show = show_map.ShowMap()
        self.flag_show_map = False
        
        # 迷路探索オブジェクト
        self.obj_search = search_maze.SearchMaze(self.mz)
        
        # 描画
        self.show_img(img3d)
        
        # ウィンドウイベントループ
        self.root.mainloop()
    
    def show_img(self, args_img):
        """ 画像を表示 """
        self.imgtk = ImageTk.PhotoImage(args_img)
        self.canvas = tk.Canvas(
                self.root, bg='black', width=const.WIDTH, height=const.HEIGHT)
        self.canvas.place(x=self.margin, y=self.margin)
        self.canvas.create_image(1, 1, anchor=tk.NW, image=self.imgtk)
    
    def msgbox_yn(self, msg):
        """ Yes/No形式のメッセージボックス表示 """
        detail = 'RANDOM SEED : ' + str(self.seed) + '\n' + \
                 '\nCURRENT FLOOR IS B' + str(self.pl.floor) + '\n' + \
                 '\nKEY COUNT : ' + str(self.count_key) + \
                 '\nSTEPS : ' + str(self.count_steps) + \
                 '\nMAPPING : ' + str(self.count_mapping) + \
                 '\nMAP IMPRESSIONS : ' + str(self.count_show_map) + \
                 '\nUP STAIRS SEARCH : ' + str(self.count_guide_up) + \
                 '\nDOWN STAIRS SEARCH : ' + str(self.count_guide_down)
        res = messagebox.askyesno(
                title=self.TITLE, message=msg, detail=detail)
        return res
    
    def key_press(self, event):
        """ キー押下イベント処理 """
        # キーリピート対策（100 = 0.1sec）
        if event.time - self.time_key < 100:
            return
        self.root.unbind('<KeyPress>', self.bind_id)
        self.time_key = event.time
        self.count_key += 1
        if self.flag_show_map:
            # 地図表示中ならば地図を閉じる
            self.flag_show_map = False
        elif event.keysym == 'Escape':
            if self.msgbox_yn('QUIT ?'):
                # 終了
                self.root.destroy()
                sys.exit()
        elif event.keysym == 'Up':
            cell_wall = self.mz.maze_wall[self.pl.y][self.pl.x]
            self.pl.move_forward(cell_wall)
            self.count_steps += 1
        elif event.keysym == 'Left':
            self.pl.turn_left()
        elif event.keysym == 'Right':
            self.pl.turn_right()
        elif event.keysym == 'Down':
            self.pl.turn_around()
        elif event.keysym == 'Prior':
            # PageUpキー
            # 上の階段判定
            cell = self.mz.maze_contents[self.pl.y][self.pl.x]
            if cell & const.EVENT_CEILING != const.MAZE_NONE:
                self.count_guide_up += 1
                if self.msgbox_yn('MOVE UP ?'):
                    # 1Fの場合
                    if self.pl.floor == 1:
                        # 迷路脱出（終了）
                        if self.msgbox_yn('ESCAPE ?'):
                            self.root.destroy()
                            sys.exit()
                    else:
                        # 上に移動
                        self.pl.floor -= 1
                        # 迷路作成
                        self.mz.back_maze(self.pl.floor)
        elif event.keysym == 'Next':
            # PageDownキー
            # 下の階段判定
            cell = self.mz.maze_contents[self.pl.y][self.pl.x]
            if cell & const.EVENT_FLOOR != const.MAZE_NONE:
                self.count_guide_down += 1
                if self.msgbox_yn('MOVE DOWN ?'):
                    # 下に移動
                    self.pl.floor += 1
                    # 迷路作成
                    self.mz.next_maze(floor=self.pl.floor)
                    self.mz.set_xy_up(
                            self.pl.x, self.pl.y, floor=self.pl.floor)
        elif (event.keysym.upper() == 'M'
                or event.keysym.upper() == 'H'
                or event.keysym.upper() == 'L'
                ):
            # 地図表示
            self.show_guide(event.keysym.upper())
            return
        # オートマッピング
        self.pl.auto_mapping()
        # 3D描画
        img3d = self.draw3d.draw(
                self.mz, self.pl.x, self.pl.y, self.pl.direction)
        self.show_img(img3d)
        self.bind_id = self.root.bind('<KeyPress>', self.key_press)
    
    def key_press_shift(self, event):
        """ Shiftキーが押されたとき """
        self.key_shift = True
    
    def key_release_shift(self, event):
        """ Shiftキーが離されたとき """
        self.key_shift = False
    
    def show_guide(self, keysymbol, player=None):
        """
        地図、経路表示
            'M' : 地図表示（通った道のみ）
            Shift + 'M' : 地図表示（全体）
            Shift + 'H' : 地図 + 上階段までの経路表示
            Shift + 'L' : 地図 + 下階段までの経路表示
        """
        self.flag_show_map = True
        if self.key_shift:
            imgmap = self.obj_show.draw_map(self.mz)
            self.count_show_map += 1
        else:
            imgmap = self.obj_show.draw_map(self.mz, player=self.pl)
            self.count_mapping += 1
        self.obj_show.draw_player(
                self.pl.x, self.pl.y, self.pl.direction)
        if keysymbol == 'H' or keysymbol == 'L':
            self.obj_search.initialize(self.mz)
            if keysymbol == 'H':
                xy_end = (self.mz.x_up, self.mz.y_up)
                self.count_guide_up += 1
            else:
                xy_end = (self.mz.x_down, self.mz.y_down)
                self.count_guide_down += 1
            self.obj_search.find_route(
                    start=(self.pl.x, self.pl.y),
                    end=xy_end,
                    direction_now=self.pl.direction)
            self.obj_show.draw_route(self.obj_search)
        self.show_img(imgmap)
        self.bind_id = self.root.bind('<KeyPress>', self.key_press)


if __name__ == "__main__":
    # 開始
    gm = Game()
    
