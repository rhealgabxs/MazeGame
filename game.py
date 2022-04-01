#!/usr/bin/env python3
"""
迷路ゲーム本体
"""
import os
import random
import shutil
import sys
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

import const
import draw
import maze
import player
import save_data
import search_maze
import show_map


class Game():
    """ ゲームクラス """
    # ウィンドウタイトル
    TITLE = 'Maze'
    
    # キーカウンタ
    count_key = {}
    
    # 地図表示の方法
    GUIDE_ONLY_ROUTE = 'ROUTE'
    GUIDE_ALL_MAP = 'ALL'
    GUIDE_UP_STAIRS = 'UP'
    GUIDE_DOWN_STAIRS = 'DOWN'
    
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
        
        # キー回数の初期化
        self.count_key['key'] = 0
        # 歩数
        self.count_key['steps'] = 0
        # オートマッピングを開いた回数
        self.count_key['mapping'] = 0
        # 全体地図を開いた回数
        self.count_key['map_all'] = 0
        # 上り階段探索を開いた回数
        self.count_key['guide_up'] = 0
        # 下り階段探索を開いた回数
        self.count_key['guide_down'] = 0
        # セーブした回数
        self.count_key['save'] = 0
        # ロードした回数
        self.count_key['load'] = 0
        
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
        self.root.unbind('<KeyPress>', self.bind_id)
        detail = ('RANDOM SEED : ' + str(self.seed)
                + '\n'
                + '\nCURRENT FLOOR IS B' + str(self.pl.floor)
                + '\n'
                + '\nKEY COUNT : ' + str(self.count_key['key'])
                + '\nSTEPS : ' + str(self.count_key['steps'])
                + '\nMAPPING : ' + str(self.count_key['mapping'])
                + '\nMAP IMPRESSIONS : ' + str(self.count_key['map_all'])
                + '\nUP STAIRS SEARCH : ' + str(self.count_key['guide_up'])
                + '\nDOWN STAIRS SEARCH : ' + str(self.count_key['guide_down'])
                + '\nSAVE : ' + str(self.count_key['save'])
                + '\nLOAD : ' + str(self.count_key['load'])
                + '')
        res = messagebox.askyesno(
                title=self.TITLE, message=msg, detail=detail)
        self.bind_id = self.root.bind('<KeyPress>', self.key_press)
        return res
    
    def key_press(self, event):
        """ キー押下イベント処理 """
        # キーリピート対策（100 = 0.1sec）
        if event.time - self.time_key < 100:
            return
        self.time_key = event.time
        if event.keysym == 'Escape':
            if self.msgbox_yn('QUIT ?'):
                # 終了
                self.root.destroy()
                sys.exit()
            return
        elif event.keysym == 'Up':
            cell_wall = self.mz.maze_wall[self.pl.y][self.pl.x]
            self.pl.move_forward(cell_wall)
            self.count_key['steps'] += 1
        elif event.keysym == 'Left':
            self.pl.turn_left()
        elif event.keysym == 'Right':
            self.pl.turn_right()
        elif event.keysym == 'Down':
            self.pl.turn_around()
        elif event.keysym == 'Prior':
            # PageUpキー
            if self.key_shift:
                # 地図 + 上階段までの経路表示
                self.show_guide(guide_type=self.GUIDE_UP_STAIRS)
                return
            # 上の階層に移動
            self.move_up_floor()
        elif event.keysym == 'Next':
            # PageDownキー
            if self.key_shift:
                # 地図 + 下階段までの経路表示
                self.show_guide(guide_type=self.GUIDE_DOWN_STAIRS)
                return
            # 下の階段に移動
            self.move_down_floor()
        elif event.keysym.upper() == 'M':
            # 地図表示
            if self.key_shift:
                self.show_guide(self.GUIDE_ALL_MAP)
            else:
                self.show_guide(self.GUIDE_ONLY_ROUTE)
            return
        elif event.keysym.upper() == 'S':
            # セーブ
            self.state_save()
        elif event.keysym.upper() == 'L':
            # ロード
            self.state_load()
        else:
            return
        self.count_key['key'] += 1
        # オートマッピング
        self.pl.auto_mapping()
        # 3D描画
        img3d = self.draw3d.draw(
                self.mz, self.pl.x, self.pl.y, self.pl.direction)
        self.show_img(img3d)
    
    def key_press_shift(self, event):
        """ Shiftキーが押されたとき """
        self.key_shift = True
    
    def key_release_shift(self, event):
        """ Shiftキーが離されたとき """
        self.key_shift = False
    
    def waiting_end(self, event):
        """ キー入力待ち終了 """
        self.root.unbind('<KeyPress>', self.bind_id_waiting)
        # 再描画
        img3d = self.draw3d.draw(
                self.mz, self.pl.x, self.pl.y, self.pl.direction)
        self.show_img(img3d)
        # キー入力イベント再開
        self.bind_id = self.root.bind('<KeyPress>', self.key_press)
    
    def move_up_floor(self):
        """ 上の階層に移動 """
        # 上の階段判定
        cell = self.mz.maze_contents[self.pl.y][self.pl.x]
        if cell & const.EVENT_CEILING != const.MAZE_NONE:
            if self.msgbox_yn('MOVE UP ?'):
                if self.pl.floor == 1:
                    # B1Fの場合
                    # 迷路脱出（終了）
                    if self.msgbox_yn('ESCAPE ?'):
                        self.root.destroy()
                        sys.exit()
                else:
                    # 上に移動
                    self.pl.floor -= 1
                    # 迷路作成
                    self.mz.back_maze(self.pl.floor)
    
    def move_down_floor(self):
        """ 下の階層に移動 """
        # 下の階段判定
        cell = self.mz.maze_contents[self.pl.y][self.pl.x]
        if cell & const.EVENT_FLOOR != const.MAZE_NONE:
            if self.msgbox_yn('MOVE DOWN ?'):
                # 下に移動
                self.pl.floor += 1
                # 迷路作成
                self.mz.next_maze(floor=self.pl.floor)
                self.mz.set_xy_up(self.pl.x, self.pl.y, floor=self.pl.floor)
    
    def show_guide(self, guide_type=GUIDE_ONLY_ROUTE):
        """ 地図、経路表示 """
        self.root.unbind('<KeyPress>', self.bind_id)
        # 地図表示
        if guide_type == self.GUIDE_ONLY_ROUTE:
            # 通った道のみ
            imgmap = self.obj_show.draw_map(self.mz, player=self.pl)
            self.count_key['mapping'] += 1
        else:
            # 全体
            imgmap = self.obj_show.draw_map(self.mz)
            self.count_key['map_all'] += 1
        # 自分の位置を表示
        self.obj_show.draw_player(self.pl.x, self.pl.y, self.pl.direction)
        # 経路表示
        if guide_type == self.GUIDE_UP_STAIRS \
                or guide_type == self.GUIDE_DOWN_STAIRS:
            if guide_type == self.GUIDE_UP_STAIRS:
                # 上階段までの経路
                xy_end = (self.mz.x_up, self.mz.y_up)
                self.count_key['guide_up'] += 1
            else:
                # 下階段までの経路
                xy_end = (self.mz.x_down, self.mz.y_down)
                self.count_key['guide_down'] += 1
            self.obj_search.initialize(self.mz)
            self.obj_search.find_route(
                    start=(self.pl.x, self.pl.y),
                    end=xy_end,
                    direction_now=self.pl.direction)
            self.obj_show.draw_route(self.obj_search)
        self.show_img(imgmap)
        # キー入力待ち
        self.bind_id_waiting = self.root.bind('<KeyPress>', self.waiting_end)
    
    def state_save(self):
        """ セーブ """
        # 確認
        if not self.msgbox_yn('SAVE ?'):
            return
        self.root.unbind('<KeyPress>', self.bind_id)
        self.count_key['save'] += 1
        # バックアップ作成
        src_file = save_data.DB_FILE
        if os.path.exists(src_file):
            filename_split = src_file.rsplit('.', 1)
            dst_file = filename_split[0] + '_bak.' + filename_split[1]
            shutil.copy2(src_file, dst_file)
        # セーブデータ接続
        obj_save = save_data.SaveData()
        # プレイヤー情報
        dic_pl = {}
        dic_pl['name'] = self.pl.name
        dic_pl['seed'] = self.seed
        dic_pl['floor'] = self.pl.floor
        dic_pl['x'] = self.pl.x
        dic_pl['y'] = self.pl.y
        dic_pl['direction'] = self.pl.direction
        obj_save.save_player(dic_pl)
        # キー回数
        dic_count = {}
        dic_count['key'] = self.count_key['key']
        dic_count['steps'] = self.count_key['steps']
        dic_count['mapping'] = self.count_key['mapping']
        dic_count['map_all'] = self.count_key['map_all']
        dic_count['guide_up'] = self.count_key['guide_up']
        dic_count['guide_down'] = self.count_key['guide_down']
        dic_count['save'] = self.count_key['save']
        dic_count['load'] = self.count_key['load']
        obj_save.save_count_key(dic_count)
        # 迷路関連
        # 分解してセーブデータ用に変換
        list_maze = []
        size_x = len(self.pl.mapping[0][0])
        size_y = len(self.pl.mapping[0])
        for i, map_floor in enumerate(self.pl.mapping):
            dic = {}
            floor = i + 1
            mapping_data = ''
            for row in map_floor:
                for cell in row:
                    if cell:
                        mapping_data += '1'
                    else:
                        mapping_data += '0'
            stairs_up_x, stairs_up_y = self.mz.stairs_up[i]
            stairs_down_x, stairs_down_y = self.mz.stairs_down[i]
            dic['floor'] = floor
            dic['size_x'] = size_x
            dic['size_y'] = size_y
            dic['mapping'] = mapping_data
            dic['stairs_up_x'] = stairs_up_x
            dic['stairs_up_y'] = stairs_up_y
            dic['stairs_down_x'] = stairs_down_x
            dic['stairs_down_y'] = stairs_down_y
            list_maze.append(dic)
        obj_save.save_maze(list_maze)
        # 乱数状態
        list_random_state = []
        for i, randstate in enumerate(self.mz.random_state):
            dic = {}
            floor = i + 1
            version = randstate[0]
            internalstate = b''
            for val in randstate[1]:
                internalstate += val.to_bytes(4, 'little')
            gauss_next = randstate[2]
            dic['floor'] = floor
            dic['version'] = version
            dic['internalstate'] = internalstate
            dic['gauss_next'] = gauss_next
            list_random_state.append(dic)
        obj_save.save_random_state(list_random_state)
        # セーブデータ接続終了
        obj_save.close_db()
        self.bind_id = self.root.bind('<KeyPress>', self.key_press)
    
    def state_load(self):
        """ ロード """
        # 確認
        if not self.msgbox_yn('LOAD ?'):
            return
        self.root.unbind('<KeyPress>', self.bind_id)
        # セーブデータ接続
        obj_save = save_data.SaveData()
        # データ読み込み
        row_pl = obj_save.load_player()
        row_count = obj_save.load_count_key()
        rows_maze = obj_save.load_maze(self.mz.width, self.mz.height)
        rows_randstate = obj_save.load_random_state()
        # セーブデータ接続終了
        obj_save.close_db()
        # 迷路関連（セーブデータの有無を調べるため最初にロード）
        if rows_maze is None or len(rows_maze) == 0:
            # セーブデータなし
            messagebox.showinfo(title=self.TITLE, message='NO SAVE DATA')
            self.bind_id = self.root.bind('<KeyPress>', self.key_press)
            return
        self.pl.mapping = []
        self.mz.stairs_up = []
        self.mz.stairs_down = []
        for row in rows_maze:
            # オートマッピング
            map_floor = []
            for y in range(self.mz.height):
                map_row = []
                for x in range(self.mz.width):
                    cell = row['mapping'][y * self.mz.height + x]
                    if cell == '1':
                        map_row.append(True)
                    else:
                        map_row.append(False)
                map_floor.append(map_row)
            self.pl.mapping.append(map_floor)
            # 上り階段
            self.mz.stairs_up.append(
                    [row['stairs_up_x'], row['stairs_up_y']])
            # 下り階段
            self.mz.stairs_down.append(
                    [row['stairs_down_x'], row['stairs_down_y']])
        # プレイヤー情報
        self.pl.name = row_pl['name']
        self.seed = row_pl['seed']
        self.pl.floor = row_pl['floor']
        self.pl.x = row_pl['x']
        self.pl.y = row_pl['y']
        self.pl.direction = row_pl['direction']
        # キー回数
        self.count_key['key'] = row_count['key']
        self.count_key['steps'] = row_count['steps']
        self.count_key['mapping'] = row_count['mapping']
        self.count_key['map_all'] = row_count['map_all']
        self.count_key['guide_up'] = row_count['guide_up']
        self.count_key['guide_down'] = row_count['guide_down']
        self.count_key['save'] = row_count['save']
        # ロード回数はカウント
        self.count_key['load'] = row_count['load'] + 1
        # 乱数状態
        self.mz.random_state = []
        for row in rows_randstate:
            version = row['version']
            data = row['internalstate']
            internalstate = []
            for i in range(0, len(data), 4):
                val = int.from_bytes(data[i:i+4], 'little')
                internalstate.append(val)
            gauss_next = row['gauss_next']
            self.mz.random_state.append(
                    (version, tuple(internalstate), gauss_next))
        # 迷路再作成
        self.mz.back_maze(self.pl.floor)
        self.bind_id = self.root.bind('<KeyPress>', self.key_press)


if __name__ == "__main__":
    # 開始
    gm = Game()
    
