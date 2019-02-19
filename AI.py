# -*- coding: utf-8 -*-

# python imports
import random

# project imports
from ks.commands import ECommandDirection, ChangeGhostDirection, ChangePacmanDirection
from ks.models import ECell, EDirection
###from graphs import Graph


ai = None

CELL_EMPTY = ECell.Empty
CELL_FOOD = ECell.Food
CELL_SUPERFOOD = ECell.SuperFood
CELL_WALL = ECell.Wall

DIR_UP = EDirection.Up
DIR_RIGHT = EDirection.Right
DIR_DOWN = EDirection.Down
DIR_LEFT = EDirection.Left



def initialize(width, height, my_score, other_score,
               board, pacman, ghosts, constants,
               my_side, other_side, current_cycle, cycle_duration):
    
    print(get_paths_for(pacman.x, pacman.y, 1, 1,1,ghosts, board, width, height));
        
    pass



def is_there_any_ghosts(x, y, board, width, height, ghosts):
    st=0
    for ghost in ghosts:
        if(ghosts[ghost.id].x== x and ghosts[ghost.id].y== y):
            st=st+1


    if st>=1 : return 1
    else : return 0




def decide(width, height, my_score, other_score,
           board, pacman, ghosts, constants,
           my_side, other_side, current_cycle, cycle_duration):


    if my_side == 'Pacman':


        TEMP=get_paths_for(pacman.x, pacman.y, 1, 1,1,ghosts, board, width, height)[0][1]
        Ysta=TEMP[0]-pacman.y;
        Xsta=TEMP[1]-pacman.x;
        
   
        if(Ysta==1):
            change_pacman_direction(DIR_DOWN)
            
        if(Ysta==-1):
            change_pacman_direction(DIR_UP)

        if(Xsta==1):
            change_pacman_direction(DIR_RIGHT)
            
        if(Xsta==-1):
            change_pacman_direction(DIR_LEFT)


    elif my_side == 'Ghost':
        for ghost in ghosts:
            change_ghost_direction(ghost.id,DIR_DOWN)


def get_paths_for(x1, y1, x2, y2, ghostscheck, ghosts, board, width, height):
    result = []
    jobs = [[[y1,x1]]]
    slen = width * height
    while(len(jobs) > 0):
        newjobs = []
        index = 0
        while(index < len(jobs)):
            
            job = jobs[index]
            x = job[-1][1]
            y = job[-1][0]
            if(x == x2 and y == y2):
                if(len(job) <= slen):
                    slen = len(job)
                    result.append(job)
                else:
                    return result
                
            else:
                if(x + 1 < width):
                    if(board[y][x + 1] != CELL_WALL and not [y, x + 1] in job):
                        if(ghostscheck):
                            if(not is_there_any_ghosts(x + 1, y, board, width, height, ghosts)):
                                newjobs.append(job + [[y, x + 1]])
                        else:    
                            newjobs.append(job + [[y, x + 1]])
                       
                if(y + 1 < height):                    
                    if(board[y + 1][x] != CELL_WALL and not [y + 1, x] in  job):
                        if(ghostscheck):
                            if(not is_there_any_ghosts(x, y + 1, board, width, height, ghosts)):
                                newjobs.append(job + [[y + 1, x]])
                        else:    
                            newjobs.append(job + [[y + 1, x]])
                                               
                if(x - 1 >= 0):
                    if(board[y][x - 1] != CELL_WALL and not [y, x - 1] in job):
                        if(ghostscheck):
                            if(not is_there_any_ghosts(x - 1, y, board, width, height, ghosts)):
                                newjobs.append(job + [[y, x - 1]])
                        else:    
                            newjobs.append(job + [[y, x - 1]])
                       
                        
                if(y - 1 >= 0):
                    if(board[y - 1][x] != CELL_WALL and not [y - 1,x] in job):
                        if(ghostscheck):
                            if(not is_there_any_ghosts(x, y - 1, board, width, height, ghosts)):
                                newjobs.append(job + [[y - 1, x]])  
                        else:    
                            newjobs.append(job + [[y - 1, x]])  
                        
            index += 1
        jobs = newjobs[:]
        


def change_pacman_direction(dir):
    ai.send_command(ChangePacmanDirection(direction=dir))


def change_ghost_direction(id, dir):
    ai.send_command(ChangeGhostDirection(id=id, direction=dir))
