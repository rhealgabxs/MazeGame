#!/usr/bin/env python3
"""
迷路作成
"""
import random

import const


class Maze():
    """ 迷路を作るクラス """
    
    # 壁
    maze_wall = []
    # 扉
    maze_door = []
    # 内容
    maze_contents = []
    # 既に堀った場所をスタックしておくための配列
    stack_path = []
    # 上り階段の位置
    x_up = 0
    y_up = 0
    # 下り階段の位置
    x_down = 0
    y_down = 0
    
    def __init__(self, width, height, seed=None, room=None):
        """ コンストラクタ """
        # 迷路の横の大きさ
        self.width = width
        # 迷路の縦の大きさ
        self.height = height
        # 乱数のシード設定
        random.seed(seed)
        # 部屋の出現確率（0-100）
        #   ※実際には設置できないことがあるので、設定数値より少ない
        self.room_init = room
        self.room_chance = room
    
    def make_maze(self):
        """ 迷路作成 """
        self.initialize()
        self.dig()
        self.finalize()
    
    def next_maze(self, random_state=None):
        """ 次の迷路を作成 """
        # 乱数の状態を戻す
        #   random.getstate()で取得した値を設定
        if random_state:
            random.setstate(random_state)
        self.make_maze()
    
    def initialize(self):
        """ 前処理 """
        # 部屋の出現確率を設定
        if self.room_init is None:
            room = random.randrange(101)
            print('room_chance = ' + str(room))
            self.room_chance = room
        # 壁で埋める
        self.maze_wall = []
        self.maze_door = []
        self.maze_contents = []
        for x in range(self.width):
            row_wall = []
            row_door = []
            row_contents = []
            for y in range(self.height):
                row_wall.append(const.MAZE_ALL)
                row_door.append(const.MAZE_NONE)
                row_contents.append(const.MAZE_NONE)
            self.maze_wall.append(row_wall)
            self.maze_door.append(row_door)
            self.maze_contents.append(row_contents)
        # 一番最初に穴を掘り始める座標をランダムに決定
        x_start_dig = random.randrange(self.width)
        y_start_dig = random.randrange(self.height)
        self.stack_path.append([x_start_dig, y_start_dig])
    
    def dig(self):
        """ 穴掘り法で迷路を作る """
        while True:
            # もし既に掘った場所で戻れる場所が無い場合、ループを抜ける
            if self.stack_path == []:
                break
            # 穴を掘り始めるxy座標をスタックからランダムにポップする
            x, y = self.stack_path.pop(random.randrange(len(self.stack_path)))
            while True:
                # 掘ることができる場所を調べる
                list_direction_dig = []
                if y - 1 >= 0:
                    if self.maze_wall[y - 1][x] == const.MAZE_ALL:
                        list_direction_dig.append(const.MAZE_NORTH)
                if x + 1 < self.width:
                    if self.maze_wall[y][x + 1] == const.MAZE_ALL:
                        list_direction_dig.append(const.MAZE_EAST)
                if y + 1 < self.height:
                    if self.maze_wall[y + 1][x] == const.MAZE_ALL:
                        list_direction_dig.append(const.MAZE_SOUTH)
                if x - 1 >= 0:
                    if self.maze_wall[y][x - 1] == const.MAZE_ALL:
                        list_direction_dig.append(const.MAZE_WEST)
                if list_direction_dig == []:
                    # 穴を掘ることが出来ない場合は、ループを抜ける
                    break
                else:
                    # 掘る方向をランダムに決定
                    direction_dig = random.choice(list_direction_dig)
                # 部屋の作成
                flag_room = self.make_room(x, y, direction_dig)
                if flag_room:
                    continue
                # 扉の作成（部屋から出るとき）
                self.make_door(x, y, direction_dig)
                # 穴を掘る
                if direction_dig == const.MAZE_NORTH:
                    self.maze_wall[y][x] &= const.MAZE_ALL ^ const.MAZE_NORTH
                    y -= 1
                    self.maze_wall[y][x] = const.MAZE_ALL ^ const.MAZE_SOUTH
                elif direction_dig == const.MAZE_EAST:
                    self.maze_wall[y][x] &= const.MAZE_ALL ^ const.MAZE_EAST
                    x += 1
                    self.maze_wall[y][x] = const.MAZE_ALL ^ const.MAZE_WEST
                elif direction_dig == const.MAZE_SOUTH:
                    self.maze_wall[y][x] &= const.MAZE_ALL ^ const.MAZE_SOUTH
                    y += 1
                    self.maze_wall[y][x] = const.MAZE_ALL ^ const.MAZE_NORTH
                elif direction_dig == const.MAZE_WEST:
                    self.maze_wall[y][x] &= const.MAZE_ALL ^ const.MAZE_WEST
                    x -= 1
                    self.maze_wall[y][x] = const.MAZE_ALL ^ const.MAZE_EAST
                # 移動先のxy座標をスタックに入れる
                self.stack_path.append([x, y])
    
    def make_room(self, x, y, direction):
        """
        部屋の作成
        戻り値：
            True  : 部屋作成あり
            False : 部屋作成なし
        """
        # 部屋の最大サイズ
        MIN_SIZE = 2
        MAX_SIZE = 5
        # MIN_SIZE周辺の場合は、部屋を作らないようにする
        if x < MIN_SIZE - 1 \
                or x > self.width - MIN_SIZE \
                or y < MIN_SIZE - 1 \
                or y > self.height - MIN_SIZE:
            return False
        # 部屋が重ならないようにする
        contents = self.maze_contents[y][x]
        if contents & const.CONTENTS_ROOM != const.MAZE_NONE:
            return False
        # 部屋の有無を決定
        if random.randrange(100) >= self.room_chance:
            return False
        # 部屋の大きさ（MIN_SIZE〜MAX_SIZE）
        size_x = random.randint(MIN_SIZE, MAX_SIZE)
        size_y = random.randint(MIN_SIZE, MAX_SIZE)
        # 扉の位置
        door_x = 0
        door_y = 0
        # 外枠から外れないようにサイズ調整（調整できない場合は終了）
        room_west = 0
        room_east = 0
        room_north = 0
        room_south = 0
        if direction == const.MAZE_NORTH:
            door_x = random.randrange(size_x)
            room_west = max(0, x - door_x)
            room_east = min(self.width, room_west + size_x)
            room_north = max(0, y + 1 - size_y)
            room_south = y + 1
        elif direction == const.MAZE_EAST:
            door_y = random.randrange(size_y)
            room_west = x
            room_east = min(self.width, room_west + size_x)
            room_north = max(0, y - door_y)
            room_south = min(self.height, room_north + size_y)
        elif direction == const.MAZE_SOUTH:
            door_x = random.randrange(size_x)
            room_west = max(0, x - door_x)
            room_east = min(self.width, room_west + size_x)
            room_north = y
            room_south = min(self.height, room_north + size_y)
        elif direction == const.MAZE_WEST:
            door_y = random.randrange(size_y)
            room_west = max(0, x + 1 - size_x)
            room_east = x + 1
            room_north = max(0, y - door_y)
            room_south = min(self.height, room_north + size_y)
        # 部屋が設置可能かどうか（未設置の場所であること）
        for room_y in range(room_north, room_south):
            for room_x in range(room_west, room_east):
                # 現在地は既に掘られているため判定から除く
                if room_x == x and room_y == y:
                    continue
                if self.maze_wall[room_y][room_x] != const.MAZE_ALL:
                    return False
        # 部屋の設置
        cell_xy = self.maze_wall[y][x]
        for room_y in range(room_north, room_south):
            for room_x in range(room_west, room_east):
                cell = const.MAZE_NONE
                # 部屋の周り
                if room_y == room_north:
                    # 上
                    cell |= const.MAZE_NORTH
                    self.stack_path.append([room_x, room_y])
                if room_y == room_south - 1:
                    # 下
                    cell |= const.MAZE_SOUTH
                    self.stack_path.append([room_x, room_y])
                if room_x == room_west:
                    # 左
                    cell |= const.MAZE_WEST
                    self.stack_path.append([room_x, room_y])
                if room_x == room_east - 1:
                    # 右
                    cell |= const.MAZE_EAST
                    self.stack_path.append([room_x, room_y])
                if room_x == x and room_y == y:
                    cell &= cell_xy
                # 設置
                self.maze_wall[room_y][room_x] = cell
                self.maze_contents[room_y][room_x] = const.CONTENTS_ROOM
        # 扉の設置
        if cell_xy != const.MAZE_ALL:
            door_xy = const.MAZE_ALL ^ cell_xy
            self.make_door(x, y, door_xy)
        # 部屋作成完了
        return True
    
    def make_door(self, x, y, direction):
        """ 扉の作成 """
        # 部屋の出入口に扉を作成
        if self.maze_contents[y][x] != const.CONTENTS_ROOM:
            return
        if direction & const.MAZE_NORTH != const.MAZE_NONE:
            self.maze_door[y][x] |= const.MAZE_NORTH
            self.maze_door[y - 1][x] |= const.MAZE_SOUTH
        if direction & const.MAZE_EAST != const.MAZE_NONE:
            self.maze_door[y][x] |= const.MAZE_EAST
            self.maze_door[y][x + 1] |= const.MAZE_WEST
        if direction & const.MAZE_SOUTH != const.MAZE_NONE:
            self.maze_door[y][x] |= const.MAZE_SOUTH
            self.maze_door[y + 1][x] |= const.MAZE_NORTH
        if direction & const.MAZE_WEST != const.MAZE_NONE:
            self.maze_door[y][x] |= const.MAZE_WEST
            self.maze_door[y][x - 1] |= const.MAZE_EAST
    
    def finalize(self):
        """ 後処理 """
        # 上り階段をセット
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        self.set_xy_up(x, y)
        # 下り階段をセット
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        self.set_xy_down(x, y)
    
    def set_xy_up(self, x, y):
        """ 上り階段の設定 """
        # 削除
        self.maze_contents[self.y_up][self.x_up] &= ~const.EVENT_CEILING
        # 設定
        self.maze_contents[y][x] |= const.EVENT_CEILING
        self.x_up = x
        self.y_up = y
    
    def set_xy_down(self, x, y):
        """ 下り階段の設定 """
        # 削除
        self.maze_contents[self.y_down][self.x_down] &= ~const.EVENT_FLOOR
        # 設定
        self.maze_contents[y][x] |= const.EVENT_FLOOR
        self.x_down = x
        self.y_down = y
    
    def print_maze(self):
        """ 迷路を表示 """
        map_print = []
        map_bottom = ''
        for iy, row in enumerate(self.maze_wall):
            map_row1 = ''
            map_row2 = ''
            for ix, cell in enumerate(row):
                door = self.maze_door[iy][ix]
                contents = self.maze_contents[iy][ix]
                map_row1 += '#'
                # 上側の壁
                if cell & const.MAZE_NORTH != const.MAZE_NONE:
                    if iy == 0:
                        map_row1 += str(ix % 10)
                    else:
                        map_row1 += '#'
                else:
                    if door & const.MAZE_NORTH != const.MAZE_NONE:
                        map_row1 += '+'
                    else:
                        map_row1 += ' '
                # 左側の壁
                if cell & const.MAZE_WEST != const.MAZE_NONE:
                    map_row2 += '#'
                else:
                    if door & const.MAZE_WEST != const.MAZE_NONE:
                        map_row2 += '+'
                    else:
                        map_row2 += ' '
                # 左端
                if ix == 0:
                    map_row2 = str(iy % 10)
                # セルの位置の状態
                if contents & const.EVENT_BOTH == const.EVENT_BOTH:
                    map_row2 += 'B'
                elif contents & const.EVENT_CEILING != const.MAZE_NONE:
                    map_row2 += 'U'
                elif contents & const.EVENT_FLOOR != const.MAZE_NONE:
                    map_row2 += 'D'
                elif contents & const.CONTENTS_ROOM != const.MAZE_NONE:
                    map_row2 += '.'
                else:
                    map_row2 += ' '
            # 右端の壁
            map_row1 += '#'
            map_row2 += str(iy % 10)
            print(map_row1)
            print(map_row2)
            if iy == 0:
                map_bottom = map_row1
        # 最下部の壁
        map_print.append(map_bottom)
        print(map_bottom)
