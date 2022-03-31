#!/usr/bin/env python3
"""
セーブデータ
"""
import os
import sqlite3

import sql


class SaveData():
    """ セーブデータクラス """
    # DBファイル名
    DB_FILE = 'save.db'
    # 今後、プレイヤー、パーティなどが複数になった場合、別IDに設定
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
        if os.path.exists(self.DB_FILE):
            flag_exists = True
        # 複数起動は考慮してないので、排他ロック
        self.conn = sqlite3.connect(self.DB_FILE, isolation_level='EXCLUSIVE')
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
            self.cur.execute(sql.SELECT_PLAYER, [self.ID])
            row = self.cur.fetchone()
        except Exception as e:
            print(e)
        return row
    
    def load_count_key(self):
        """ ロード（キー回数） """
        row = None
        try:
            self.cur.execute(sql.SELECT_COUNT_KEY, [self.ID])
            row = self.cur.fetchone()
        except Exception as e:
            print(e)
        return row
    
    def load_maze(self, size_x, size_y):
        """ ロード（迷路関連） """
        row = None
        try:
            self.cur.execute(sql.SELECT_MAZE, [self.ID, size_x, size_y])
            rows = self.cur.fetchall()
        except Exception as e:
            print(e)
        return rows
    
    def load_random_state(self):
        """ ロード（乱数状態） """
        row = None
        try:
            self.cur.execute(sql.SELECT_RANDOM_STATE, [self.ID])
            rows = self.cur.fetchall()
        except Exception as e:
            print(e)
        return rows
    
    # セーブ
    def save_player(self, list_data):
        """ セーブ（プレイヤー情報） """
        try:
            row = self.load_player()
            if row is None:
                list_data.insert(0, self.ID)
                self.cur.execute(sql.INSERT_PLAYER, list_data)
            else:
                list_data.append(self.ID)
                self.cur.execute(sql.UPDATE_PLAYER, list_data)
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.conn.commit()
    
    def save_count_key(self, list_data):
        """ セーブ（キー回数） """
        try:
            row = self.load_count_key()
            if row is None:
                list_data.insert(0, self.ID)
                self.cur.execute(sql.INSERT_COUNT_KEY, list_data)
            else:
                list_data.append(self.ID)
                self.cur.execute(sql.UPDATE_COUNT_KEY, list_data)
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.conn.commit()
    
    def save_maze(self, list_data):
        """ セーブ（迷路関連） """
        try:
            for row_data in list_data:
                floor = row_data[0]
                self.cur.execute(sql.SELECT_MAZE_BY_KEY, [self.ID, floor])
                row = self.cur.fetchone()
                if row is None:
                    insert_data = [self.ID, floor]
                    insert_data.extend(row_data[1:])
                    self.cur.execute(sql.INSERT_MAZE, insert_data)
                else:
                    update_data = row_data[1:]
                    update_data.extend([self.ID, floor])
                    self.cur.execute(sql.UPDATE_MAZE, update_data)
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.conn.commit()
    
    def save_random_state(self, list_data):
        """ セーブ（乱数状態） """
        try:
            for row_data in list_data:
                floor = row_data[0]
                self.cur.execute(
                        sql.SELECT_RANDOM_STATE_BY_KEY, [self.ID, floor])
                row = self.cur.fetchone()
                if row is None:
                    insert_data = [self.ID, floor]
                    insert_data.extend(row_data[1:])
                    self.cur.execute(sql.INSERT_RANDOM_STATE, insert_data)
                else:
                    update_data = row_data[1:]
                    update_data.extend([self.ID, floor])
                    self.cur.execute(sql.UPDATE_RANDOM_STATE, update_data)
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.conn.commit()

