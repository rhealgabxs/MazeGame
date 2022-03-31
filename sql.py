"""
SQL
"""

# 新規DB作成時のCREATE TABLE
CREATE_TABLE = '''
CREATE TABLE player (
      id INTEGER PRIMARY KEY
    , name TEXT
    , seed INTEGER
    , floor INTEGER
    , x INTEGER
    , y INTEGER
    , direction INTEGER
);

CREATE TABLE count_key (
      id INTEGER PRIMARY KEY
    , key INTEGER
    , steps INTEGER
    , mapping INTEGER
    , map_all INTEGER
    , guide_up INTEGER
    , guide_down INTEGER
    , save INTEGER
    , load INTEGER
);

CREATE TABLE maze (
      id INTEGER
    , floor INTEGER
    , size_x INTEGER
    , size_y INTEGER
    , mapping TEXT
    , stairs_up_x INTEGER
    , stairs_up_y INTEGER
    , stairs_down_x INTEGER
    , stairs_down_y INTEGER
    , PRIMARY KEY(id, floor)
);

CREATE TABLE random_state (
      id INTEGER
    , floor INTEGER
    , version INTEGER
    , internalstate BLOB
    , gauss_next BLOB
    , PRIMARY KEY(id, floor)
);
'''

# プレイヤー情報テーブルSQL
SELECT_PLAYER = '''
SELECT *
FROM player
WHERE id = ?
'''
INSERT_PLAYER = '''
INSERT INTO player
VALUES (?, ?, ?, ?, ?, ?, ?)
'''
UPDATE_PLAYER = '''
UPDATE player
SET   name = ?
    , seed = ?
    , floor = ?
    , x = ?
    , y = ?
    , direction = ?
WHERE id = ?
'''

# キー回数テーブルSQL
SELECT_COUNT_KEY = '''
SELECT *
FROM count_key
WHERE id = ?
'''
INSERT_COUNT_KEY = '''
INSERT INTO count_key
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
'''
UPDATE_COUNT_KEY = '''
UPDATE count_key
SET   key = ?
    , steps = ?
    , mapping = ?
    , map_all = ?
    , guide_up = ?
    , guide_down = ?
    , save = ?
    , load = ?
WHERE id = ?
'''

# 迷路関連テーブルSQL
# サイズ指定しているのは、異なる大きさのデータは読めないようにするため
SELECT_MAZE = '''
SELECT *
FROM maze
WHERE id = ?
  AND size_x = ?
  AND size_y = ?
ORDER BY floor
'''
SELECT_MAZE_BY_KEY = '''
SELECT *
FROM maze
WHERE id = ?
  AND floor = ?
'''
INSERT_MAZE = '''
INSERT INTO maze
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
'''
UPDATE_MAZE = '''
UPDATE maze
SET   size_x = ?
    , size_y = ?
    , mapping = ?
    , stairs_up_x = ?
    , stairs_up_y = ?
    , stairs_down_x = ?
    , stairs_down_y = ?
WHERE id = ?
  AND floor = ?
'''

# 乱数状態テーブルSQL
SELECT_RANDOM_STATE = '''
SELECT *
FROM random_state
WHERE id = ?
ORDER BY floor
'''
SELECT_RANDOM_STATE_BY_KEY = '''
SELECT *
FROM random_state
WHERE id = ?
  AND floor = ?
'''
INSERT_RANDOM_STATE = '''
INSERT INTO random_state
VALUES (?, ?, ?, ?, ?)
'''
UPDATE_RANDOM_STATE = '''
UPDATE random_state
SET   version = ?
    , internalstate = ?
    , gauss_next = ?
WHERE id = ?
  AND floor = ?
'''

