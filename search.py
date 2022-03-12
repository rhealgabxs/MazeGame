#!/bin/env python3
"""
迷路探索
"""
import collections

import const


class SearchMaze():
    """ 迷路探索クラス """
    
    # 探索した歩数情報
    maze_step = None
    # 経路
    route = None
    
    def __init__(self, obj_maze):
        """
        コンストラクタ
        引数：
            obj_maze   迷路オブジェクト
        """
        # 壁情報
        self.map_wall = obj_maze.maze_wall
        # 探索開始位置
        self.x_start = obj_maze.x_up
        self.y_start = obj_maze.y_up
        # 探索終了位置
        self.x_end = obj_maze.x_down
        self.y_end = obj_maze.y_down
    
    def find_route(self, start=None, end=None, direction_now=None):
        """
        探索経路を見つける
            幅優先探索した後、逆順をたどる
        引数：
            start   開始位置（タプル(x, y)）
            end     終了位置（タプル(x, y)）
            direction_now   現在の向き（直線優先にするため）
        """
        # 開始位置
        if start is not None:
            self.x_start, self.y_start = start
        # 終了位置
        if end is not None:
            self.x_end, self.y_end = end
        # 迷路探索
        #   ゴール→スタートで幅優先探索する
        #   経路作成で直線優先方向が逆になるため
        self.breadth_first((self.x_end, self.y_end))
        
        # 探索方向
        DIRECTION_ALL = [const.MAZE_NORTH, const.MAZE_EAST, 
                         const.MAZE_SOUTH, const.MAZE_WEST]
        # 優先する探索方向
        direction_priority = const.MAZE_NORTH
        if direction_now is not None:
            direction_priority = direction_now
        
        # 経路の開始位置
        x = self.x_start
        y = self.y_start
        step = self.maze_step[y][x]
        step_end = step + 1
        self.route = [(step_end - step, x, y)]
        # 経路作成
        while step > 1:
            # 複数候補がある場合は直線優先
            direction_list = DIRECTION_ALL[:]
            direction_list.remove(direction_priority)
            direction_list.insert(0, direction_priority)
            # 移動可能方向
            cell = self.map_wall[y][x]
            x_next = x
            y_next = y
            for direction in direction_list:
                x_next = x
                y_next = y
                if direction == const.MAZE_NORTH:
                    y_next -= 1
                elif direction == const.MAZE_EAST:
                    x_next += 1
                elif direction == const.MAZE_SOUTH:
                    y_next += 1
                elif direction == const.MAZE_WEST:
                    x_next -= 1
                # 通路判定
                if cell & direction == const.MAZE_NONE:
                    step_next = self.maze_step[y_next][x_next]
                    if step_next == step - 1:
                        x = x_next
                        y = y_next
                        step = step_next
                        self.route.append((step_end - step, x, y))
                        direction_priority = direction
                        break
    
    def breadth_first(self, start=None):
        """
        幅優先探索
        引数：
            start   探索開始位置（タプル(x, y)）
        """
        # 探索開始の位置
        x = self.x_start
        y = self.y_start
        if start is not None:
            x, y = start
        
        # 訪問場所の歩数の初期化
        self.maze_step = [[0 for i in range(len(self.map_wall[0]))]
                             for j in range(len(self.map_wall))]
        
        # 歩数
        step = 1
        # 開始場所に歩数を入れる
        self.maze_step[y][x] = step
        # キューに追加
        q = collections.deque([(step, x, y)])
        
        while len(q) > 0:
            step, x, y = q.popleft()
            step += 1
            # 各方向を調べる
            cell = self.map_wall[y][x]
            for direction in (const.MAZE_NORTH, const.MAZE_EAST, 
                              const.MAZE_SOUTH, const.MAZE_WEST):
                x_next = x
                y_next = y
                if direction == const.MAZE_NORTH:
                    y_next -= 1
                elif direction == const.MAZE_EAST:
                    x_next += 1
                elif direction == const.MAZE_SOUTH:
                    y_next += 1
                elif direction == const.MAZE_WEST:
                    x_next -= 1
                # 通路判定
                if cell & direction == const.MAZE_NONE:
                    # 未訪問判定
                    if self.maze_step[y_next][x_next] == 0:
                        self.maze_step[y_next][x_next] = step
                        q.append((step, x_next, y_next))


if __name__ == "__main__":
    # テスト
    import maze
    
    seed = 123
    print('random.seed = ' + str(seed))
    room = 100
    print('room_chance = ' + str(room))
    mz = maze.Maze(20, 20, seed=seed, room=room)
    mz.make_maze()
    mz.print_maze()
    print()
    
    s = SearchMaze(mz)
    """
    s.breadth_first((10, 10))
    #s.find_route()
    str0 = '    '
    for iy, row in enumerate(s.maze_step):
        # 先頭行
        if iy == 0:
            for ix in range(len(row)):
                str0 += str(ix).rjust(4, ' ')
            print(str0)
        # 内容
        str_row = str(iy).zfill(2) + ' : '
        for ix, cell in enumerate(row):
            str_row += str(cell).zfill(3)
            if ix < len(row) - 1:
                str_row += ','
        print(str_row)
        # 最終行
        if iy == len(row) - 1:
            print(str0)
    """
    s.find_route()
    for r in s.route:
        print(r)
    #"""

