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
WHERE id = :id
'''
INSERT_PLAYER = '''
INSERT INTO player
VALUES (
    :id
  , :name
  , :seed
  , :floor
  , :x
  , :y
  , :direction
)
'''
UPDATE_PLAYER = '''
UPDATE player
SET name = :name
  , seed = :seed
  , floor = :floor
  , x = :x
  , y = :y
  , direction = :direction
WHERE id = :id
'''

# キー回数テーブルSQL
SELECT_COUNT_KEY = '''
SELECT *
FROM count_key
WHERE id = :id
'''
INSERT_COUNT_KEY = '''
INSERT INTO count_key
VALUES (
    :id
  , :key
  , :steps
  , :mapping
  , :map_all
  , :guide_up
  , :guide_down
  , :save
  , :load
)
'''
UPDATE_COUNT_KEY = '''
UPDATE count_key
SET key = :key
  , steps = :steps
  , mapping = :mapping
  , map_all = :map_all
  , guide_up = :guide_up
  , guide_down = :guide_down
  , save = :save
  , load = :load
WHERE id = :id
'''

# 迷路関連テーブルSQL
# サイズ指定しているのは、異なる大きさのデータは読めないようにするため
SELECT_MAZE = '''
SELECT *
FROM maze
WHERE id = :id
  AND size_x = :size_x
  AND size_y = :size_y
ORDER BY floor
'''
SELECT_MAZE_BY_KEY = '''
SELECT *
FROM maze
WHERE id = :id
  AND floor = :floor
'''
INSERT_MAZE = '''
INSERT INTO maze
VALUES (
    :id
  , :floor
  , :size_x
  , :size_y
  , :mapping
  , :stairs_up_x
  , :stairs_up_y
  , :stairs_down_x
  , :stairs_down_y
)
'''
UPDATE_MAZE = '''
UPDATE maze
SET size_x = :size_x
  , size_y = :size_y
  , mapping = :mapping
  , stairs_up_x = :stairs_up_x
  , stairs_up_y = :stairs_up_y
  , stairs_down_x = :stairs_down_x
  , stairs_down_y = :stairs_down_y
WHERE id = :id
  AND floor = :floor
'''

# 乱数状態テーブルSQL
SELECT_RANDOM_STATE = '''
SELECT *
FROM random_state
WHERE id = :id
ORDER BY floor
'''
SELECT_RANDOM_STATE_BY_KEY = '''
SELECT *
FROM random_state
WHERE id = :id
  AND floor = :floor
'''
INSERT_RANDOM_STATE = '''
INSERT INTO random_state
VALUES (
    :id
  , :floor
  , :version
  , :internalstate
  , :gauss_next
)
'''
UPDATE_RANDOM_STATE = '''
UPDATE random_state
SET version = :version
  , internalstate = :internalstate
  , gauss_next = :gauss_next
WHERE id = :id
  AND floor = :floor
'''

