#!/usr/bin/env python3
"""
セーブデータ
"""
import os
import sqlite3

import sql


# DBファイル名
DB_FILE = 'save.db'


class SaveData():
    """ セーブデータクラス """
    # 今後、プレイヤー、パーティなどが複数になった場合、別IDに設定
    #   ID >= 2 をバックアップに使うのもありかも
    ID = 1
    
    def __init__(self):
        """ コンストラクタ """
        self.connect_db()
    
    def __def__(self):
        """ デストラクタ """
        self.close_db()
    
    def connect_db(self):
        """ DB接続 """
        flag_exists = False
        if os.path.exists(DB_FILE):
            flag_exists = True
        # 複数起動は考慮してないので、排他ロック
        self.conn = sqlite3.connect(DB_FILE, isolation_level='EXCLUSIVE')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        # 新規ならテーブル作成
        if not flag_exists:
            self.cur.executescript(sql.CREATE_TABLE)
            self.conn.commit()
    
    def close_db(self):
        """ DB接続終了 """
        self.cur.close()
        self.conn.close()
    
    # ロード
    def load_player(self):
        """ ロード（プレイヤー情報） """
        row = None
        try:
            dic = {'id' : self.ID}
            self.cur.execute(sql.SELECT_PLAYER, dic)
            row = self.cur.fetchone()
        except Exception as e:
            print(e)
        return row
    
    def load_count_key(self):
        """ ロード（キー回数） """
        row = None
        try:
            dic = {'id' : self.ID}
            self.cur.execute(sql.SELECT_COUNT_KEY, dic)
            row = self.cur.fetchone()
        except Exception as e:
            print(e)
        return row
    
    def load_maze(self, size_x, size_y):
        """ ロード（迷路関連） """
        row = None
        try:
            dic = {'id' : self.ID}
            dic['size_x'] = size_x
            dic['size_y'] = size_y
            self.cur.execute(sql.SELECT_MAZE, dic)
            rows = self.cur.fetchall()
        except Exception as e:
            print(e)
        return rows
    
    def load_random_state(self):
        """ ロード（乱数状態） """
        row = None
        try:
            dic = {'id' : self.ID}
            self.cur.execute(sql.SELECT_RANDOM_STATE, dic)
            rows = self.cur.fetchall()
        except Exception as e:
            print(e)
        return rows
    
    # セーブ
    def save_player(self, dic):
        """ セーブ（プレイヤー情報） """
        try:
            dic['id'] = self.ID
            row = self.load_player()
            if row is None:
                self.cur.execute(sql.INSERT_PLAYER, dic)
            else:
                self.cur.execute(sql.UPDATE_PLAYER, dic)
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.conn.commit()
    
    def save_count_key(self, dic):
        """ セーブ（キー回数） """
        try:
            dic['id'] = self.ID
            row = self.load_count_key()
            if row is None:
                self.cur.execute(sql.INSERT_COUNT_KEY, dic)
            else:
                self.cur.execute(sql.UPDATE_COUNT_KEY, dic)
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.conn.commit()
    
    def save_maze(self, list_data):
        """ セーブ（迷路関連） """
        try:
            for dic in list_data:
                dic['id'] = self.ID
                self.cur.execute(sql.SELECT_MAZE_BY_KEY, dic)
                row = self.cur.fetchone()
                if row is None:
                    self.cur.execute(sql.INSERT_MAZE, dic)
                else:
                    self.cur.execute(sql.UPDATE_MAZE, dic)
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.conn.commit()
    
    def save_random_state(self, list_data):
        """ セーブ（乱数状態） """
        try:
            for dic in list_data:
                dic['id'] = self.ID
                self.cur.execute(sql.SELECT_RANDOM_STATE_BY_KEY, dic)
                row = self.cur.fetchone()
                if row is None:
                    self.cur.execute(sql.INSERT_RANDOM_STATE, dic)
                else:
                    self.cur.execute(sql.UPDATE_RANDOM_STATE, dic)
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.conn.commit()

