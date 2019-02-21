# ChillinWARS

ChillinWars 2019

AIChallenge CUP


    ____                  ____                     ______  _                 
   |  _ \                / __ \                   |  ____|| |                
   | |_) | _   _   __ _ | |  | |__   __ ___  _ __ | |__   | |  ___ __      __
   |  _ < | | | | / _` || |  | |\ \ / // _ \| '__||  __|  | | / _ \\ \ /\ / /
   | |_) || |_| || (_| || |__| | \ V /|  __/| |   | |     | || (_) |\ V  V / 
   |____/  \__,_| \__, | \____/   \_/  \___||_|   |_|     |_| \___/  \_/\_/  
                   __/ |                                                     
                  |___/                                                      
                                                      _____    
                                            /\       |_   _|   
                  _ __ ___      __ _       /  \        | |     
                 | '_ ` _ \    / _` |     / /\ \       | |     
                 | | | | | | _| (_| | _  / ____ \  _  _| |_  _ 
                 |_| |_| |_|(_)\__,_|(_)/_/    \_\(_)|_____|(_)
                                                               
                    Arash Rezaee           Mohammad Chegini
        
https://chillinwars.ir

$$$  Main File is AI.py


FrontEnd Functions:

  *Gmove --> ID , X , Y , GhostCheck
  
  
     ## have PathFind inside
     
     ## have GDirChange inside (Ghost Changing Dir is limited by this Function we will find solution)
     
    
  *Pmove --> X , Y , GhostCheck
  
  
     ## have PathFind inside
     
     
    
  *IsGhost --> X,Y
  
  
     ## AutoConnecting to another Function called is_there_any_ghost
     
     
  
  *GDirChange --> ID , dir
  
  
     ## AutoConnecting to Global Function called GhostDirChangingGLOBAL
  
 
 
 BackEnd Functions:
 
    *FindPath
    
    ## FindPATH(OBJECT, x2, y2, ghostscheck, ghosts, board, width, height):
    
    
    *GhostDirChangingGLOBAL 
