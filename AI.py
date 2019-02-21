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
    
    pass


def decide(width, height, my_score, other_score,
           board, pacman, ghosts, constants,
           my_side, other_side, current_cycle, cycle_duration):

    print()
    def GDirChange(ID,dir):
        GhostDirChangingGLOBAL(ID,dir,ghosts,board)
    def IsGhost(X,Y):
        is_there_any_ghost(X, Y, board, width, height, ghosts)

    def IsPacman(X,Y):
        is_there_pacman(X, Y, board, width, height, ghosts)
        
    def PMove(X,Y,Gcheck):
        TEMP=FindPATH(pacman, X, Y,Gcheck,ghosts, board, width, height,'nor')[1]
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
            
    def GMove(ID,X,Y,Gcheck,status):
        
        PATH=FindPATH(ghosts[ID], X, Y,Gcheck,ghosts, board, width, height,status)[1]
        Ysta=PATH[0]-ghosts[ID].y;
        Xsta=PATH[1]-ghosts[ID].x;
        if(Ysta==1):    ##DOWN
            GDirChange(ID,'d')
        if(Ysta==-1):##بالا   
            GDirChange(ID,'u')
        if(Xsta==1):  ##RIGHT
            GDirChange(ID,'r')
        if(Xsta==-1):  ##LEFT  
            GDirChange(ID,'l')
    


###### **** PACMAN ****
            
    if my_side == 'Pacman':
        PMove(1,1,1)




###### **** GHOST ****
    elif my_side == 'Ghost':

        for ID in range(0,len(ghosts)):
            GMove(ID,pacman.x,pacman.y,1,'nor')
 

            
            













def GhostDirChangingGLOBAL(ID,DIR,ghosts,board):
######################## MOVE DOWN
    if DIR== 'd':
        
        if(ghosts[ID].direction==DIR_UP):

            if(board[ghosts[ID].y][ghosts[ID].x-1] != CELL_WALL and board[ghosts[ID].y][ghosts[ID].x+1] != CELL_WALL):  ## CAN GO right OR left
                change_ghost_direction(ID,random.choice([DIR_LEFT,DIR_RIGHT]))
                        
            if(board[ghosts[ID].y][ghosts[ID].x-1] == CELL_WALL and board[ghosts[ID].y][ghosts[ID].x+1] != CELL_WALL):  ## CAN GO RIGHT 
                change_ghost_direction(ID,DIR_RIGHT)
                        
            if(board[ghosts[ID].y][ghosts[ID].x-1] != CELL_WALL and board[ghosts[ID].y][ghosts[ID].x+1] == CELL_WALL):  ## CAN GO LEFT 
                change_ghost_direction(ID,DIR_LEFT)

            if(board[ghosts[ID].y][ghosts[ID].x-1] == CELL_WALL and board[ghosts[ID].y][ghosts[ID].x+1] == CELL_WALL):  ## Nothing To do
                print("Nothing To do")

            if(board[ghosts[ID].y-1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y][ghosts[ID].x-1] == CELL_WALL ):
                change_ghost_direction(ID,DIR_DOWN)
        else:
                change_ghost_direction(ID,DIR_DOWN)
                

########################    MOVE UP

    if DIR== 'u':
    
        if(ghosts[ID].direction==DIR_DOWN):

            if(board[ghosts[ID].y][ghosts[ID].x-1] != CELL_WALL and board[ghosts[ID].y][ghosts[ID].x+1] != CELL_WALL):  ## CAN GO right OR left
                change_ghost_direction(ID,random.choice([DIR_LEFT,DIR_RIGHT]))
                        
            if(board[ghosts[ID].y][ghosts[ID].x-1] == CELL_WALL and board[ghosts[ID].y][ghosts[ID].x+1] != CELL_WALL):  ## CAN GO RIGHT 
                change_ghost_direction(ID,DIR_RIGHT)
                        
            if(board[ghosts[ID].y][ghosts[ID].x-1] != CELL_WALL and board[ghosts[ID].y][ghosts[ID].x+1] == CELL_WALL):  ## CAN GO LEFT 
                change_ghost_direction(ID,DIR_LEFT)

            if(board[ghosts[ID].y][ghosts[ID].x-1] == CELL_WALL and board[ghosts[ID].y][ghosts[ID].x+1] == CELL_WALL):  ## Nothing To do
                print("Nothing To do")

            if(board[ghosts[ID].y-1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y+1][ghosts[ID].x] == CELL_WALL and board[ghosts[ID].y][ghosts[ID].x-1] == CELL_WALL ):
                change_ghost_direction(ID,DIR_UP)
        else:
                change_ghost_direction(ID,DIR_UP)

                

#######################     MOVE RIGHT

    if DIR=='r':
        
    
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
    if DIR=='l':
        
    
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


                
    

def FindPATH(OBJECT, x2, y2, ghostscheck, ghosts, board, width, height,status):
    ### in pacman path finding status is nor Auto

    ## but in Ghost mode you have to put it 
    if (status=='nor'):  ## Pacman is not GIANT
        paths = [[[OBJECT.y, OBJECT.x]]]
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

    else:  ## Running From Pacman
        
        paths = [[[OBJECT.y, OBJECT.x]]]
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
                                if(not is_there_pacman(x + 1, y, board, width, height, ghosts)):
                                    newpaths.append(path + [[y, x + 1]])
                                    used.append([y, x + 1])
                            else:
                                newpaths.append(path + [[y, x + 1]])
                                used.append([y, x + 1])
                            
                    if(y + 1 < height):                    
                        if(board[y + 1][x] != CELL_WALL and not [y + 1, x] in (path + used)):
                            if(ghostscheck):
                                if(not is_there_pacman(x, y + 1, board, width, height, ghosts)):
                                    newpaths.append(path + [[y + 1, x]])
                                    used.append([y + 1, x])
                            else:    
                                newpaths.append(path + [[y + 1, x]])
                                used.append([y + 1, x])                  
                    if(x - 1 >= 0):
                        if(board[y][x - 1] != CELL_WALL and not [y, x - 1] in (path + used)):
                            if(ghostscheck):
                                if(not is_there_pacman(x - 1, y, board, width, height, ghosts)):
                                    newpaths.append(path + [[y, x - 1]])
                                    used.append([y, x - 1])
                            else:    
                                newpaths.append(path + [[y, x - 1]])
                                used.append([y, x - 1])
                        
                    if(y - 1 >= 0):
                        if(board[y - 1][x] != CELL_WALL and not [y - 1,x] in (path + used)):
                            if(ghostscheck):
                                if(not is_there_pacman(x, y - 1, board, width, height, ghosts)):
                                    newpaths.append(path + [[y - 1, x]])
                                    used.append([y - 1, x])
                            else:    
                                newpaths.append(path + [[y - 1, x]])  
                                used.append([y - 1, x])  
                index += 1    
            paths = newpaths[:]
        
            total_paths = len(paths)
        return []        


def is_there_any_ghost(x, y, board, width, height, ghosts):
    st=0
    for ID in range(0,len(ghosts)):
        if(ghosts[ID].x== x and ghosts[ID].y== y):
            st=st+1
    if st>=1 : return 1
    else : return 0

def is_there_pacman(x,y,board, width, height, ghosts):
    if(pacman.x==x and pacman.y==y):
        return 1
    else:
        return 0

def change_pacman_direction(dir):
    ai.send_command(ChangePacmanDirection(direction=dir))


def change_ghost_direction(id, dir):
    ai.send_command(ChangeGhostDirection(id=id, direction=dir))
