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


    change_ghost_direction(0,DIR_DOWN)
    pass



def is_there_any_ghost(x, y, board, width, height, ghosts):
    st=0
    for ghost in ghosts:
        if(ghosts[ghost.id].x== x and ghosts[ghost.id].y== y):
            st=st+1


    if st>=1 : return 1
    else : return 0


def gmove(ID,DIR,ghosts,board):
######################## MOVE DOWN
    if DIR== down:
        
        if(ghosts[ID].direction==DIR_UP):
            if(board[ghosts[ID].y][ghosts[ID].x-1]==CELL_WALL):
                change_ghost_direction(ID,DIR_RIGHT)
                        
            else:
                if(board[ghosts[ID].y][ghosts[ID].x+1]==CELL_WALL):
                    change_ghost_direction(ID,DIR_LEFT)
                else:
                    change_ghost_direction(ID,DIR_DOWN) 

        else:
            change_ghost_direction(ID,DIR_DOWN)

########################    MOVE UP

    if DIR== up:
    
        if(ghosts[ID].direction==DIR_DOWN):
            if(board[ghosts[ID].y][ghosts[ID].x-1]==CELL_WALL):
                change_ghost_direction(ID,DIR_RIGHT)
                        
            else:
                if(board[ghosts[ID].y][ghosts[ID].x+1]==CELL_WALL):
                    change_ghost_direction(ID,DIR_LEFT)
                else:
                    change_ghost_direction(ID,DIR_UP) 

        else:
                change_ghost_direction(ID,DIR_UP)

                

#######################     MOVE RIGHT

    if DIR==right:
        
    
        if(ghosts[ID].direction==DIR_LEFT):
            if(board[ghosts[ID].y-1][ghosts[ID].x] != CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] != CELL_WALL):  ## CAN GO UP OR DOWN
                change_ghost_direction(ID,random.choice([DIR_UP,DIR_DOWN]))
                        
            if(board[ghosts[ID].y-1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] != CELL_WALL):  ## CAN GO UP 
                change_ghost_direction(ID,DIR_UP)
                        
            if(board[ghosts[ID].y-1][ghosts[ID].x] != CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] == CELL_WALL):  ## CAN GO DOWN 
                change_ghost_direction(ID,DIR_UP)

            if(board[ghosts[ID].y-1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] == CELL_WALL):  ## Nothing To do
                print("Nothing To do")

            if(board[ghosts[ID].y-1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y][ghosts[ID].x-1] == CELL_WALL ):
                change_ghost_direction(ID,DIR_RIGHT)

        else:
                change_ghost_direction(ID,DIR_RIGHT)

#######################     MOVE LEFT     
    if DIR==left:
        
    
        if(ghosts[ID].direction==DIR_RIGHT):
            
            if(board[ghosts[ID].y-1][ghosts[ID].x] != CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] != CELL_WALL):  ## CAN GO UP OR DOWN
                change_ghost_direction(ID,random.choice([DIR_UP,DIR_DOWN]))
                        
            if(board[ghosts[ID].y-1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] != CELL_WALL):  ## CAN GO UP 
                change_ghost_direction(ID,DIR_UP)
                        
            if(board[ghosts[ID].y-1][ghosts[ID].x] != CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] == CELL_WALL):  ## CAN GO DOWN 
                change_ghost_direction(ID,DIR_UP)

            if(board[ghosts[ID].y-1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] == CELL_WALL):  ## Nothing To do
                print("Nothing To do")

            if(board[ghosts[ID].y-1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y][ghosts[ID].x+1] == CELL_WALL ):
                change_ghost_direction(ID,DIR_LEFT)

        else:
                change_ghost_direction(ID,DIR_LEFT)


                
                

def decide(width, height, my_score, other_score,
           board, pacman, ghosts, constants,
           my_side, other_side, current_cycle, cycle_duration):

##########################################
    if my_side == 'Pacman':
        print("ds")

############################################################################################
    elif my_side == 'Ghost':



### everyBody Fuck PACMAN:
        
        for ID in range(0,4):
            print("as ",ID)
            TEMP=find_pacman_path_to_xy(ghosts[ID], pacman.x, pacman.y,1,ghosts, board, width, height)[1]
        
            Ysta=TEMP[0]-ghosts[ID].y;
            Xsta=TEMP[1]-ghosts[ID].x;
        
   
            if(Ysta==1):    ##DOWN

                gmove(ID,down,ghosts,board)

            
            if(Ysta==-1):##بالا
                
                gmove(ID,up,ghosts,board)
                



            if(Xsta==1):  ##RIGHT
                 gmove(ID,right,ghosts,board)

            if(Xsta==-1):  ##LEFT
                
                 gmove(ID,left,ghosts,board)

            
            

def find_pacman_path_to_xy(pacman, x2, y2, ghostscheck, ghosts, board, width, height):
    paths = [[[pacman.y, pacman.x]]]
    total_paths = len(paths)
    used = []
    while(total_paths > 0):
        newpaths = []
        index = 0
        while(index < total_paths):         
            path = paths[index]
            x = path[-1][1]
            y = path[-1][0]
            if(x == x2 and y == y2):
                return path
                
            else:
                if(x + 1 < width):
                    if(board[y][x + 1] != CELL_WALL and not [y, x + 1] in (path + used)):
                        if(ghostscheck):
                            if(not is_there_any_ghost(x + 1, y, board, width, height, ghosts)):
                                newpaths.append(path + [[y, x + 1]])
                                used.append([y, x + 1])
                        else:
                            newpaths.append(path + [[y, x + 1]])
                            used.append([y, x + 1])
                            
                if(y + 1 < height):                    
                    if(board[y + 1][x] != CELL_WALL and not [y + 1, x] in (path + used)):
                        if(ghostscheck):
                            if(not is_there_any_ghost(x, y + 1, board, width, height, ghosts)):
                                newpaths.append(path + [[y + 1, x]])
                                used.append([y + 1, x])
                        else:    
                            newpaths.append(path + [[y + 1, x]])
                            used.append([y + 1, x])                  
                if(x - 1 >= 0):
                    if(board[y][x - 1] != CELL_WALL and not [y, x - 1] in (path + used)):
                        if(ghostscheck):
                            if(not is_there_any_ghost(x - 1, y, board, width, height, ghosts)):
                                newpaths.append(path + [[y, x - 1]])
                                used.append([y, x - 1])
                        else:    
                            newpaths.append(path + [[y, x - 1]])
                            used.append([y, x - 1])
                        
                if(y - 1 >= 0):
                    if(board[y - 1][x] != CELL_WALL and not [y - 1,x] in (path + used)):
                        if(ghostscheck):
                            if(not is_there_any_ghost(x, y - 1, board, width, height, ghosts)):
                                newpaths.append(path + [[y - 1, x]])
                                used.append([y - 1, x])
                        else:    
                            newpaths.append(path + [[y - 1, x]])  
                            used.append([y - 1, x])  
            index += 1    
        paths = newpaths[:]
        
        total_paths = len(paths)
    return []



def change_pacman_direction(dir):
    ai.send_command(ChangePacmanDirection(direction=dir))


def change_ghost_direction(id, dir):
    ai.send_command(ChangeGhostDirection(id=id, direction=dir))
