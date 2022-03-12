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
    TITLE = 'Maze'
    
    def __init__(self):
        """ コンストラクタ """
        # 画面と描画領域の余白
        self.margin = (const.WIN_W - const.WIDTH) // 2
        
        self.root = tk.Tk()
        self.root.title(self.TITLE)
        self.root.geometry(str(const.WIN_W) + 'x' + str(const.WIN_H))
        self.root.configure(bg='black')
        self.bind_id = self.root.bind('<KeyPress>', self.key_handler)
        
        # 迷路作成
        seed = time.time_ns() % (10 ** 9)
        #seed = 123
        print('random.seed = ' + str(seed))
        random.seed(seed)
        self.random_state = [random.getstate()]
        #self.mz = maze.Maze(100, 100, seed=seed, room=100)
        self.mz = maze.Maze(20, 20, seed=seed)
        self.mz.make_maze()
        self.random_state.append(random.getstate())
        
        # プレイヤー作成
        self.pl = player.Player('Player')
        # スタート位置決定
        self.pl.x = self.mz.x_up
        self.pl.y = self.mz.y_up
        self.pl.direction = random.choice(
                [const.DIR_NORTH, const.DIR_EAST, 
                 const.DIR_SOUTH, const.DIR_WEST])
        
        # 3D描画オブジェクト
        self.draw3d = draw.Draw3D()
        img3d = self.draw3d.draw(
                self.mz, self.pl.x, self.pl.y, self.pl.direction)
        
        # 地図描画オブジェクト
        self.obj_show = show_map.ShowMap()
        
        # 迷路探索オブジェクト
        self.obj_search = search_maze.SearchMaze(self.mz)
        
        # 描画
        self.show_img(img3d)
        
        # メインループ
        self.root.mainloop()
    
    def show_img(self, args_img):
        """ 画像を表示 """
        self.imgtk = ImageTk.PhotoImage(args_img)
        self.canvas = tk.Canvas(
                self.root, bg='black', width=const.WIDTH, height=const.HEIGHT)
        self.canvas.place(x=self.margin, y=self.margin)
        self.canvas.create_image(1, 1, anchor=tk.NW, image=self.imgtk)
    
    def key_handler(self, event):
        """ キーイベント処理 """
        if event.keysym == 'Escape':
            # ESCキー
            self.root.unbind('<KeyPress>', self.bind_id)
            res = messagebox.askyesno(
                    title=self.TITLE, message='QUIT ?',
                    detail='CURRENT FLOOR IS B' + str(self.pl.floor))
            if res:
                self.root.destroy()
                sys.exit()
            self.bind_id = self.root.bind('<KeyPress>', self.key_handler)
        elif event.keysym == 'Up':
            cell_wall = self.mz.maze_wall[self.pl.y][self.pl.x]
            self.pl.move_forward(cell_wall)
        elif event.keysym == 'Left':
            self.pl.turn_left()
        elif event.keysym == 'Right':
            self.pl.turn_right()
        elif event.keysym == 'Down':
            self.pl.turn_around()
        elif event.keysym == 'a':
            # 地図＋経路表示
            imgmap = self.obj_show.draw_all(self.mz)
            self.obj_show.draw_player(
                    self.pl.x, self.pl.y, self.pl.direction)
            self.obj_search.initialize(self.mz)
            self.obj_search.find_route(
                    start=(self.pl.x, self.pl.y),
                    end=(self.mz.x_down, self.mz.y_down),
                    direction_now=self.pl.direction)
            self.obj_show.draw_route(self.obj_search)
            self.show_img(imgmap)
            return
        elif event.keysym == 'm':
            # 地図表示
            imgmap = self.obj_show.draw_all(self.mz)
            self.obj_show.draw_player(
                    self.pl.x, self.pl.y, self.pl.direction)
            self.show_img(imgmap)
            return
        elif event.keysym == 'Prior':
            # PageUpキー
            # 上の階段判定
            cell = self.mz.maze_contents[self.pl.y][self.pl.x]
            if cell & const.EVENT_CEILING != const.MAZE_NONE:
                self.root.unbind('<KeyPress>', self.bind_id)
                res = messagebox.askyesno(
                        title=self.TITLE, message='MOVE UP ?', 
                        detail='CURRENT FLOOR IS B' + str(self.pl.floor))
                if res:
                    # 1Fの場合
                    if self.pl.floor == 1:
                        # 迷路脱出（終了）
                        res = messagebox.askyesno(
                                title=self.TITLE, message='ESCAPE ?')
                        if res:
                            self.root.destroy()
                            sys.exit()
                    else:
                        # 上に移動
                        self.pl.floor -= 1
                        # 迷路作成
                        stat = self.random_state[self.pl.floor - 1]
                        self.mz.next_maze(random_state=stat)
                self.bind_id = self.root.bind('<KeyPress>', self.key_handler)
        elif event.keysym == 'Next':
            # PageDownキー
            # 下の階段判定
            cell = self.mz.maze_contents[self.pl.y][self.pl.x]
            if cell & const.EVENT_FLOOR != const.MAZE_NONE:
                self.root.unbind('<KeyPress>', self.bind_id)
                res = messagebox.askyesno(
                        title=self.TITLE, message='MOVE DOWN ?', 
                        detail='CURRENT FLOOR IS B' + str(self.pl.floor))
                if res:
                    # 下に移動
                    self.pl.floor += 1
                    # 迷路作成
                    stat = self.random_state[self.pl.floor - 1]
                    self.mz.next_maze(random_state=stat)
                    self.mz.set_xy_up(self.pl.x, self.pl.y)
                    if len(self.random_state) <= self.pl.floor:
                        self.random_state.append(random.getstate())
                self.bind_id = self.root.bind('<KeyPress>', self.key_handler)
        else:
            pass
        # 3D描画
        img3d = self.draw3d.draw(
                self.mz, self.pl.x, self.pl.y, self.pl.direction)
        self.show_img(img3d)


if __name__ == "__main__":
    # 開始
    gm = Game()
    
