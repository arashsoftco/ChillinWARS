import random
import copy
from ks.commands import ECommandDirection, ChangeGhostDirection, ChangePacmanDirection
from ks.models import ECell, EDirection

ai = None

CELL_EMPTY = ECell.Empty
CELL_FOOD = ECell.Food
CELL_SUPERFOOD = ECell.SuperFood
CELL_WALL = ECell.Wall

DIR_UP = EDirection.Up
DIR_RIGHT = EDirection.Right
DIR_DOWN = EDirection.Down
DIR_LEFT = EDirection.Left

food = [[]]
super_food = [[]]
super_food_for_ghosts = [[]]
ghost_is_triggered = 0
distance_to_ghost_memory = [100, 100, 100]


def initialize(width, height, my_score, other_score,
               board, pacman, ghosts, constants,
               my_side, other_side, current_cycle, cycle_duration):
    food.pop(0)
    super_food.pop(0)
    super_food_for_ghosts.pop(0)

    for x in range(width):
        for y in range(height):
            if board[y][x] == CELL_FOOD:
                food.append([y, x])

    for x in range(width):
        for y in range(height):
            if board[y][x] == CELL_SUPERFOOD:
                super_food.append([y, x])

    for x in range(width):
        for y in range(height):
            if board[y][x] == CELL_SUPERFOOD:
                super_food_for_ghosts.append([y, x])

    pass


def decide(width, height, my_score, other_score,
           board, pacman, ghosts, constants,
           my_side, other_side, current_cycle, cycle_duration):
    global ghost_is_triggered
    food_map_copy = 0
    food_board = copy.deepcopy(board)

    def nearest_ghost():
        minimum_distance = 100000
        for id in range(len(ghosts)):
            temp = len(FindPATH(pacman, ghosts[id].x, ghosts[id].y, 0, ghosts, board, width, height, 'nor', pacman))
            if temp < minimum_distance:
                minimum_distance = temp
        return minimum_distance

    def nearest_ghost_id():
        target_id = 0
        minimum_distance = 100000
        for id in range(len(ghosts)):
            temp = len(FindPATH(pacman, ghosts[id].x, ghosts[id].y, 0, ghosts, board, width, height, 'nor', pacman))
            if temp < minimum_distance:
                minimum_distance = temp
                target_id = id

        return target_id

    def pacman_move(path):
        desiredY = path[0] - pacman.y
        desiredX = path[1] - pacman.x

        if is_there_any_ghost(desiredX,desiredY,board,width,height,ghosts):
            if pacman.direction == DIR_RIGHT:
                change_pacman_direction(DIR_LEFT)
            if pacman.direction == DIR_LEFT:
                change_pacman_direction(DIR_RIGHT)
            if pacman.direction == DIR_DOWN:
                change_pacman_direction(DIR_UP)
            if pacman.direction == DIR_UP:
                change_pacman_direction(DIR_DOWN)
            return

        if desiredX == 1:
            change_pacman_direction(DIR_RIGHT)
        if desiredX == -1:
            change_pacman_direction(DIR_LEFT)
        if desiredY == 1:
            change_pacman_direction(DIR_DOWN)
        if desiredY == -1:
            change_pacman_direction(DIR_UP)

    def pacman_eat_food():
        print('pacman_eat_food')
        if food_map_copy == 0:
            map_copy_food()

        path = find_path_to_nearst_food(pacman, CELL_FOOD, 1, ghosts, food_board, width, height)[1]
        pacman_move(path)

    def pacman_eat_super_food():
        print('pacman_eat_super_food')

        if [pacman.x, pacman.y] in super_food:
            for counter in range(len(super_food)):
                if pacman.x == super_food[1] and pacman.y == super_food[0]:
                    super_food.pop(counter)

        if len(super_food):
            path = find_path_to_nearst_food(pacman, CELL_SUPERFOOD, 1, ghosts, board, width, height)[1]
            pacman_move(path)
        else:
            pacman_eat_food()

    def map_copy_food():
        for x in range(width):
            for y in range(height):
                if board[y][x] == CELL_SUPERFOOD:
                    food_board[y][x] = CELL_WALL

    def pacman_attack():
        global ghost_is_triggered
        ghost_is_triggered = 0
        print('pacman_attack')
        id = nearest_ghost_id()
        path = pacman_attack_path(id, ghosts, board, width, height, pacman)[1]
        pacman_move(path)

    def distance_to_super_foods():
        if len(super_food_for_ghosts) == 0:
            return 0

        distance = 1000

        for iterator in range(len(super_food_for_ghosts)):
            temp_super_food = super_food_for_ghosts[iterator]
            temp = len(FindPATH(pacman, temp_super_food[1], temp_super_food[0], 1, ghosts, board, width, height, 'nor',
                                pacman))
            if temp < distance:
                distance = temp

        if [pacman.x, pacman.y] in super_food_for_ghosts:
            for counter in range(len(super_food_for_ghosts)):
                if pacman.x == super_food_for_ghosts[1] and pacman.y == super_food_for_ghosts[0]:
                    super_food_for_ghosts.pop(counter)
        print('in distance to super foods', distance)
        return distance

    def ghost_move(id, path):

        desiredY = path[0] - ghosts[id].y
        desiredX = path[1] - ghosts[id].x

        if desiredX == 1:
            change_ghost_direction(id, DIR_RIGHT)
            if ghosts[id].direction == DIR_LEFT:
                if board[ghosts[id].y][ghosts[id].x + 1] == CELL_WALL:
                    change_ghost_direction(id, DIR_RIGHT)

                if board[ghosts[id].y+1][ghosts[id].x] == CELL_WALL:
                    change_ghost_direction(id, DIR_UP)
                else:
                    change_ghost_direction(id, DIR_DOWN)

        if desiredX == -1:
            change_ghost_direction(id, DIR_LEFT)
            if ghosts[id].direction == DIR_RIGHT:
                if board[ghosts[id].y][ghosts[id].x - 1] == CELL_WALL:
                    change_ghost_direction(id, DIR_LEFT)

                if board[ghosts[id].y+1][ghosts[id].x] == CELL_WALL:
                    change_ghost_direction(id, DIR_UP)
                else:
                    change_ghost_direction(id, DIR_DOWN)

        if desiredY == 1:
            change_ghost_direction(id, DIR_DOWN)
            if ghosts[id].direction == DIR_UP:
                if board[ghosts[id].y - 1][ghosts[id].x] == CELL_WALL:
                    change_ghost_direction(id, DIR_DOWN)

                if board[ghosts[id].y][ghosts[id].x+1] == CELL_WALL:
                    change_ghost_direction(id, DIR_LEFT)
                else:
                    change_ghost_direction(id, DIR_RIGHT)

        if desiredY == -1:
            change_ghost_direction(id, DIR_UP)
            if ghosts[id].direction == DIR_DOWN:
                if board[ghosts[id].y + 1][ghosts[id].x] == CELL_WALL:
                    change_ghost_direction(id, DIR_UP)

                if board[ghosts[id].y][ghosts[id].x+1] == CELL_WALL:
                    change_ghost_direction(id, DIR_LEFT)
                else:
                    change_ghost_direction(id, DIR_RIGHT)

    def ghost_run_away():
        ghost_run_away_board = copy.deepcopy(board)

        if pacman.direction == DIR_DOWN:
            ghost_run_away_board[pacman.y - 1][pacman.x] = CELL_WALL

        if pacman.direction == DIR_UP:
            ghost_run_away_board[pacman.y + 1][pacman.x] = CELL_WALL

        if pacman.direction == DIR_LEFT:
            ghost_run_away_board[pacman.y][pacman.x + 1] = CELL_WALL

        if pacman.direction == DIR_RIGHT:
            ghost_run_away_board[pacman.y][pacman.x - 1] = CELL_WALL

        if pacman.x < width / 2 and pacman.y < height / 2:
            for id in range(len(ghosts)):
                path = FindPATH(ghosts[id], width - 2, height - 2, 0, ghosts,
                                ghost_run_away_board, width, height, 'em', pacman)
                if len(path) == 0:
                    change_ghost_direction(id, random.choice([DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN]))
                    return
                ghost_move(id, path[1])

        if pacman.x < width / 2 and pacman.y > height / 2:
            for id in range(len(ghosts)):
                path = FindPATH(ghosts[id], width - 2, 1, 0, ghosts,
                                ghost_run_away_board, width, height, 'em', pacman)
                if len(path) == 0:
                    change_ghost_direction(id, random.choice([DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN]))
                    return
                ghost_move(id, path[1])

        if pacman.x > width / 2 and pacman.y < height / 2:
            for id in range(len(ghosts)):
                path = FindPATH(ghosts[id], 1, height - 2, 0, ghosts,
                                ghost_run_away_board, width, height, 'em', pacman)
                if len(path) == 0:
                    change_ghost_direction(id, random.choice([DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN]))
                    return
                ghost_move(id, path[1])

        if pacman.x > width / 2 and pacman.y > height / 2:
            for id in range(len(ghosts)):
                path = FindPATH(ghosts[id], 1, 1, 0, ghosts,
                                ghost_run_away_board, width, height, 'em', pacman)
                if len(path) == 0:
                    change_ghost_direction(id, random.choice([DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN]))
                    return
                ghost_move(id, path[1])

    def ghosts_attack():

        path_for_ghost_three = 0
        path_for_ghost_zero = FindPATH(ghosts[0], pacman.x, pacman.y, 0, ghosts, board, width, height, 'nor', pacman)[1]
        path_for_ghost_one = ghost_attack_path0(1, ghosts, board, width, height, pacman)[1]
        path_for_ghost_two = FindPATH(ghosts[2], pacman.x, pacman.y, 0, ghosts, board, width, height, 'nor', pacman)[1]

        if current_cycle % 50 == 0:
            if path_for_ghost_zero == FindPATH(ghosts[0], pacman.x, pacman.y, 0, ghosts, board, width, height, 'nor', pacman)[1]:
                path_for_ghost_zero = ghost_attack_path0(0, ghosts, board, width, height, pacman)[1]
            else:
                path_for_ghost_zero = FindPATH(ghosts[0], pacman.x, pacman.y, 0, ghosts, board, width, height, 'nor', pacman)[1]

        if len(ghosts) == 4:
            path_for_ghost_three = ghost_attack_path0(3, ghosts, board, width, height, pacman)[1]

        ghost_move(0, path_for_ghost_zero)

        ghost_move(1, path_for_ghost_one)

        ghost_move(2, path_for_ghost_two)

        if len(ghosts) == 4:
            ghost_move(3, path_for_ghost_three)

    if my_side == 'Pacman':

        min_dist_ghosts = nearest_ghost()
        distance_to_ghost_memory.append(min_dist_ghosts)

        if len(distance_to_ghost_memory) >= 3:
            distance_to_ghost_memory.pop(0)

        if distance_to_ghost_memory[2] < 6 and distance_to_ghost_memory[1] >= distance_to_ghost_memory[2] and \
                distance_to_ghost_memory[0] >= distance_to_ghost_memory[1]:
            ghost_is_triggered = 1

        if pacman.giant_form_remaining_time > 4:
            pacman_attack()
        else:

            if ghost_is_triggered:
                pacman_eat_super_food()
            else:
                pacman_eat_food()

    elif my_side == 'Ghost':
        should_run = False

        if pacman.giant_form_remaining_time > 4:
            should_run = True
        else:
            should_run = False

        nearest_super_food = distance_to_super_foods()
        if nearest_super_food < 8:
            should_run = True

        if should_run:
            ghost_run_away()
        else:
            ghosts_attack()


def change_pacman_direction(dir):
    ai.send_command(ChangePacmanDirection(direction=dir))


def change_ghost_direction(id, dir):
    ai.send_command(ChangeGhostDirection(id=id, direction=dir))


def FindPATH(OBJECT, x2, y2, ghostscheck, ghosts, board, width, height, status, pacman):
    if status == 'nor':
        paths = [[[OBJECT.y, OBJECT.x]]]
        total_paths = len(paths)
        used = []
        while total_paths > 0:
            newpaths = []
            index = 0
            while index < total_paths:
                path = paths[index]
                x = path[-1][1]
                y = path[-1][0]
                if x == x2 and y == y2:
                    return path

                else:
                    if x + 1 < width:
                        if board[y][x + 1] != CELL_WALL and not [y, x + 1] in (path + used):
                            if ghostscheck:
                                if not is_there_any_ghost(x + 1, y, board, width, height, ghosts):
                                    newpaths.append(path + [[y, x + 1]])
                                    used.append([y, x + 1])
                            else:
                                newpaths.append(path + [[y, x + 1]])
                                used.append([y, x + 1])

                    if y + 1 < height:
                        if board[y + 1][x] != CELL_WALL and not [y + 1, x] in (path + used):
                            if ghostscheck:
                                if not is_there_any_ghost(x, y + 1, board, width, height, ghosts):
                                    newpaths.append(path + [[y + 1, x]])
                                    used.append([y + 1, x])
                            else:
                                newpaths.append(path + [[y + 1, x]])
                                used.append([y + 1, x])
                    if x - 1 >= 0:
                        if board[y][x - 1] != CELL_WALL and not [y, x - 1] in (path + used):
                            if (ghostscheck):
                                if not is_there_any_ghost(x - 1, y, board, width, height, ghosts):
                                    newpaths.append(path + [[y, x - 1]])
                                    used.append([y, x - 1])
                            else:
                                newpaths.append(path + [[y, x - 1]])
                                used.append([y, x - 1])

                    if y - 1 >= 0:
                        if board[y - 1][x] != CELL_WALL and not [y - 1, x] in (path + used):
                            if ghostscheck:
                                if not is_there_any_ghost(x, y - 1, board, width, height, ghosts):
                                    newpaths.append(path + [[y - 1, x]])
                                    used.append([y - 1, x])
                            else:
                                newpaths.append(path + [[y - 1, x]])
                                used.append([y - 1, x])
                index += 1
            paths = copy.deepcopy(newpaths)
            total_paths = len(paths)
        return []

    else:
        print("Escape")
        ghostscheck = 1
        paths = [[[OBJECT.y, OBJECT.x]]]
        total_paths = len(paths)
        used = []
        while total_paths > 0:
            newpaths = []
            index = 0
            while index < total_paths:
                path = paths[index]
                x = path[-1][1]
                y = path[-1][0]
                if x == x2 and y == y2:
                    return path

                else:
                    if x + 1 < width:
                        if board[y][x + 1] != CELL_WALL and not [y, x + 1] in (path + used):
                            if (1):
                                if not is_there_pacman(x + 1, y, board, width, height, pacman):
                                    newpaths.append(path + [[y, x + 1]])
                                    used.append([y, x + 1])
                            else:
                                newpaths.append(path + [[y, x + 1]])
                                used.append([y, x + 1])

                    if y + 1 < height:
                        if board[y + 1][x] != CELL_WALL and not [y + 1, x] in (path + used):
                            if (1):
                                if not is_there_pacman(x, y + 1, board, width, height, pacman):
                                    newpaths.append(path + [[y + 1, x]])
                                    used.append([y + 1, x])
                            else:
                                newpaths.append(path + [[y + 1, x]])
                                used.append([y + 1, x])
                    if x - 1 >= 0:
                        if board[y][x - 1] != CELL_WALL and not [y, x - 1] in (path + used):
                            if (1):
                                if not is_there_pacman(x - 1, y, board, width, height, pacman):
                                    newpaths.append(path + [[y, x - 1]])
                                    used.append([y, x - 1])
                            else:
                                newpaths.append(path + [[y, x - 1]])
                                used.append([y, x - 1])

                    if y - 1 >= 0:
                        if board[y - 1][x] != CELL_WALL and not [y - 1, x] in (path + used):
                            if (1):
                                if not is_there_pacman(x, y - 1, board, width, height, pacman):
                                    newpaths.append(path + [[y - 1, x]])
                                    used.append([y - 1, x])
                            else:
                                newpaths.append(path + [[y - 1, x]])
                                used.append([y - 1, x])
                index += 1

            paths = copy.deepcopy(newpaths)
            total_paths = len(paths)
        return []


def is_there_any_ghost(x, y, board, width, height, ghosts):
    st = 0
    for ID in range(0, len(ghosts)):
        if ghosts[ID].x == x and ghosts[ID].y == y:
            st = st + 1
    if st >= 1:
        return 1
    else:
        return 0


def is_there_pacman(x, y, board, width, height, pacman):
    if pacman.x == x and pacman.y == y:
        return 1
    else:
        return 0


def find_path_to_nearst_food(pacman, food_type, ghostscheck, ghosts, board, width, height):
    paths = [[[pacman.y, pacman.x]]]
    total_paths = len(paths)
    used = []
    wboard = copy.deepcopy(board)

    while total_paths > 0:
        newpaths = []
        index = 0
        while index < total_paths:
            path = paths[index]
            x = path[-1][1]
            y = path[-1][0]
            if wboard[y][x] == food_type:
                return path

            else:
                if x + 1 < width:
                    if board[y][x + 1] != CELL_WALL and not [y, x + 1] in (path + used):
                        if ghostscheck:
                            if not is_there_any_ghost(x + 1, y, board, width, height, ghosts):
                                newpaths.append(path + [[y, x + 1]])
                                used.append([y, x + 1])
                        else:
                            newpaths.append(path + [[y, x + 1]])
                            used.append([y, x + 1])

                if y + 1 < height:
                    if board[y + 1][x] != CELL_WALL and not [y + 1, x] in (path + used):
                        if ghostscheck:
                            if not is_there_any_ghost(x, y + 1, board, width, height, ghosts):
                                newpaths.append(path + [[y + 1, x]])
                                used.append([y + 1, x])
                        else:
                            newpaths.append(path + [[y + 1, x]])
                            used.append([y + 1, x])
                if x - 1 >= 0:
                    if board[y][x - 1] != CELL_WALL and not [y, x - 1] in (path + used):
                        if ghostscheck:
                            if not is_there_any_ghost(x - 1, y, board, width, height, ghosts):
                                newpaths.append(path + [[y, x - 1]])
                                used.append([y, x - 1])
                        else:
                            newpaths.append(path + [[y, x - 1]])
                            used.append([y, x - 1])

                if y - 1 >= 0:
                    if board[y - 1][x] != CELL_WALL and not [y - 1, x] in (path + used):
                        if ghostscheck:
                            if not is_there_any_ghost(x, y - 1, board, width, height, ghosts):
                                newpaths.append(path + [[y - 1, x]])
                                used.append([y - 1, x])
                        else:
                            newpaths.append(path + [[y - 1, x]])
                            used.append([y - 1, x])
            index += 1
        paths = copy.deepcopy(newpaths)

        total_paths = len(paths)
    return []


def pacman_attack_path(ID, ghosts, board, width, height, pacman):
    paths = [[[pacman.y, pacman.x]]]
    total_paths = len(paths)
    used = []

    EditedBoard = copy.deepcopy(board)

    if ghosts[ID].direction == DIR_DOWN:
        EditedBoard[ghosts[ID].y - 1][ghosts[ID].x] = CELL_WALL

    if ghosts[ID].direction == DIR_UP:
        EditedBoard[ghosts[ID].y + 1][ghosts[ID].x] = CELL_WALL

    if ghosts[ID].direction == DIR_LEFT:
        EditedBoard[ghosts[ID].y][ghosts[ID].x + 1] = CELL_WALL

    if ghosts[ID].direction == DIR_RIGHT:
        EditedBoard[ghosts[ID].y][ghosts[ID].x - 1] = CELL_WALL

    while total_paths > 0:
        newpaths = []
        index = 0
        while index < total_paths:
            path = paths[index]
            x = path[-1][1]
            y = path[-1][0]
            if x == ghosts[ID].x and y == ghosts[ID].y:
                return path

            else:
                if x + 1 < width:
                    if EditedBoard[y][x + 1] != CELL_WALL and not [y, x + 1] in (path + used):
                        newpaths.append(path + [[y, x + 1]])
                        used.append([y, x + 1])
                if y + 1 < height:
                    if EditedBoard[y + 1][x] != CELL_WALL and not [y + 1, x] in (path + used):
                        newpaths.append(path + [[y + 1, x]])
                        used.append([y + 1, x])
                if x - 1 >= 0:
                    if EditedBoard[y][x - 1] != CELL_WALL and not [y, x - 1] in (path + used):
                        newpaths.append(path + [[y, x - 1]])
                        used.append([y, x - 1])
                if y - 1 >= 0:
                    if EditedBoard[y - 1][x] != CELL_WALL and not [y - 1, x] in (path + used):
                        newpaths.append(path + [[y - 1, x]])
                        used.append([y - 1, x])

            index += 1
        paths = copy.deepcopy(newpaths)
        total_paths = len(paths)
    return []


def ghost_attack_path(id, ghosts, board, width, height, pacman):
    paths = [[[ghosts[id].y, ghosts[id].x]]]
    total_paths = len(paths)
    used = []

    edited_board = copy.deepcopy(board)

    if pacman.direction == DIR_DOWN:
        edited_board[pacman.y - 1][pacman.x] = CELL_WALL

    if pacman.direction == DIR_UP:
        edited_board[pacman.y + 1][pacman.x] = CELL_WALL

    if pacman.direction == DIR_LEFT:
        edited_board[pacman.y][pacman.x + 1] = CELL_WALL

    if pacman.direction == DIR_RIGHT:
        edited_board[pacman.y][pacman.x - 1] = CELL_WALL

    while total_paths > 0:
        newpaths = []
        index = 0
        while index < total_paths:
            path = paths[index]
            x = path[-1][1]
            y = path[-1][0]
            if x == ghosts[id].x and y == ghosts[id].y:
                return path

            else:
                if x + 1 < width:
                    if edited_board[y][x + 1] != CELL_WALL and not [y, x + 1] in (path + used):
                        newpaths.append(path + [[y, x + 1]])
                        used.append([y, x + 1])
                if y + 1 < height:
                    if edited_board[y + 1][x] != CELL_WALL and not [y + 1, x] in (path + used):
                        newpaths.append(path + [[y + 1, x]])
                        used.append([y + 1, x])
                if x - 1 >= 0:
                    if edited_board[y][x - 1] != CELL_WALL and not [y, x - 1] in (path + used):
                        newpaths.append(path + [[y, x - 1]])
                        used.append([y, x - 1])
                if y - 1 >= 0:
                    if edited_board[y - 1][x] != CELL_WALL and not [y - 1, x] in (path + used):
                        newpaths.append(path + [[y - 1, x]])
                        used.append([y - 1, x])

            index += 1
            paths = copy.deepcopy(newpaths)
            total_paths = len(paths)
        return []


def ghost_attack_path0(id, ghosts, board, width, height, pacman):
    paths = [[[ghosts[id].y, ghosts[id].x]]]
    total_paths = len(paths)
    used = []

    EditedBoard = copy.deepcopy(board)

    if pacman.direction == DIR_DOWN:
        EditedBoard[pacman.y - 1][pacman.x] = CELL_WALL

    if pacman.direction == DIR_UP:
        EditedBoard[pacman.y + 1][pacman.x] = CELL_WALL

    if pacman.direction == DIR_LEFT:
        EditedBoard[pacman.y][pacman.x + 1] = CELL_WALL

    if pacman.direction == DIR_RIGHT:
        EditedBoard[pacman.y][pacman.x - 1] = CELL_WALL

    while total_paths > 0:
        newpaths = []
        index = 0
        while index < total_paths:
            path = paths[index]
            x = path[-1][1]
            y = path[-1][0]
            if x == pacman.x and y == pacman.y:
                return path

            else:
                if x + 1 < width:
                    if EditedBoard[y][x + 1] != CELL_WALL and not [y, x + 1] in (path + used):
                        newpaths.append(path + [[y, x + 1]])
                        used.append([y, x + 1])
                if y + 1 < height:
                    if EditedBoard[y + 1][x] != CELL_WALL and not [y + 1, x] in (path + used):
                        newpaths.append(path + [[y + 1, x]])
                        used.append([y + 1, x])
                if x - 1 >= 0:
                    if EditedBoard[y][x - 1] != CELL_WALL and not [y, x - 1] in (path + used):
                        newpaths.append(path + [[y, x - 1]])
                        used.append([y, x - 1])
                if y - 1 >= 0:
                    if EditedBoard[y - 1][x] != CELL_WALL and not [y - 1, x] in (path + used):
                        newpaths.append(path + [[y - 1, x]])
                        used.append([y - 1, x])

            index += 1
        paths = copy.deepcopy(newpaths)
        total_paths = len(paths)
    return []
