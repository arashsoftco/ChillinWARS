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


Functions:

  Gmove --> ID , X , Y , GhostCheck
      have PathFind inside
      have GDirChange inside (Ghost Changing Dir is limited by this Function we will find solution)
    
  Pmove --> X , Y , GhostCheck
      have PathFind inside
    
  IsGhost --> X,Y
      Related to another Function
  
  GDirChange --> ID , dir
      Realated to Global Function GhostDirChangingGLOBAL
  
 
