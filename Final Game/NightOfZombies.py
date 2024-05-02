import pygame, simpleGE, random, json

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("house.png")
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 60
        self.score = 0
        self.lifes = 5
        
        
        
        self.numLives = numLives()
        self.lblScore = LblScore()
        self.lblTime = LblTime()
        self.soldier = Soldier(self)
        self.NUM_BULLETS = 15
        self.currentBullet = 0       
        self.bullets = []
        
        for i in range(self.NUM_BULLETS):
            self.bullets.append(Bullet(self, self.soldier)) 
        
        self.zombies = []
        
            
        for i in range(6):
            self.zombies.append(Zombie(self))
        
        self.sprites = [self.soldier, self.zombies, self.lblScore, 
        self.lblTime,self.bullets,self.numLives]
        self.sndZombie = simpleGE.Sound("Zombie Sound.wav")
        
    def processEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.currentBullet += 1
                if self.currentBullet >= self.NUM_BULLETS:
                    self.currentBullet = 0
                self.bullets[self.currentBullet].fire()
    
    def process(self):
        for zombie in self.zombies:
            if self.soldier.collidesWith(zombie):
                self.lifes -= 1
                self.numLives.text = f"Lives: {self.lifes}"
                zombie.reset()
                if self.lifes < 0:
                    self.timer.totalTime = -1   
            for b in self.bullets:
                if b.collidesWith(zombie):
                    self.sndZombie.play()
                    zombie.reset()
                    self.score += 1
                    self.lblScore.text = f"Score: {self.score}"       
        
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Final Score: {self.score}")
            self.stop()

class Intro(simpleGE.Scene):
    def __init__(self, score = 0):
        super().__init__()
        self.setImage("house.png")
        self.status = "quit" 
        self.score = score
        
        if self.score == 0:
            
            self.lblInstructions = simpleGE.MultiLabel()
            self.lblInstructions.textLines = [
            "Welcome to the Amazing Zombie hunt game!! ",
            "use the arrowkeys to move",
            "Use the spacebar and X to shoot",
            "avoid and shoot the zombies before time runs out"]
            self.lblInstructions.center = (320, 240)
            self.lblInstructions.size = (600, 200)
            self.lblInstructions.clearBack = True
            self.lblInstructions.fgColor = ((0x66, 0x14, 0xFF))
            
            self.btnPlay = simpleGE.Button()
            self.btnPlay.center = (150, 400)
            self.btnPlay.text = "Play"
            
            self.btnQuit = simpleGE.Button()
            self.btnQuit.center = (500, 400)
            self.btnQuit.text = "Quit"
        else:
            
            self.lblInstructions = simpleGE.MultiLabel()
            self.lblInstructions.textLines = [
            "Congradulations you have completed a hunt! ",
            "Not too shabby but I could do better!",
            "Try Again?????"]
            self.lblInstructions.center = (320, 240)
            self.lblInstructions.size = (500, 200)
            
            
            self.btnPlay = simpleGE.Button()
            self.btnPlay.center = (150, 400)
            self.btnPlay.text = "Try again"
            
        self.lblScore = simpleGE.Label()
        self.lblInstructions.clearBack = True
        self.lblScore.center = (320, 100)
        self.lblScore.size = (200, 30)
        self.lblScore.text = f"Previous Score: {self.score}"
        
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (500, 400)
        self.btnQuit.text = "Quit"
        
        self.sprites = [
            self.lblScore,
            self.lblInstructions,
            self.btnPlay,
            self.btnQuit
            ]

    def process(self):
        if self.btnPlay.clicked:
            self.status = "play"
            self.stop()
        if self.btnQuit.clicked:
            self.status = "quit"
            self.stop()
            

class leaderBoard(simpleGE.Scene):
    def __init__(self, score = 0):
        super().__init__()
        self.setImage("house.png") 
        self.status = "quit"
        self.score = score
        # leaderBoard.loadScores()
        
        self.lblScore = simpleGE.Label()
        self.lblScore.center = (320, 100)
        self.lblScore.size = (220, 30)
        self.lblScore.text = f"Previous Score: {self.score}"
        
        self.btnName = simpleGE.TxtInput()
        self.btnName.center = (320, 400)
        self.btnName.text = "Enter name"
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.center = (150, 400)
        self.btnPlay.text = "Try again"
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (500, 400)
        self.btnQuit.text = "Quit"
        
        self.board = simpleGE.Label()
        self.board .center = (320, 130)
        self.board .size = (220, 30)
        self.board .text = "Leaderboard"
        #slot 1
        self.scoreSlot1 = simpleGE.Label()
        self.scoreSlot1.center = (220, 162)
        self.scoreSlot1.size = (200, 30)
        self.scoreSlot1.text = "slot1"
        
        self.scoreSlot12 = simpleGE.Label()
        self.scoreSlot12.center = (420 ,162)
        self.scoreSlot12.size = (200, 30)
        self.scoreSlot12.text = "slot1/2"
        #slot 2
        self.scoreSlot2 = simpleGE.Label()
        self.scoreSlot2.center = (220, 194)
        self.scoreSlot2.size = (200, 30)
        self.scoreSlot2.text = "slot2"
        
        self.scoreSlot22 = simpleGE.Label()
        self.scoreSlot22.center = (420 ,194)
        self.scoreSlot22.size = (200, 30)
        self.scoreSlot22.text = "slot2/2"
        #slot 3
        self.scoreSlot3 = simpleGE.Label()
        self.scoreSlot3.center = (220, 226)
        self.scoreSlot3.size = (200, 30)
        self.scoreSlot3.text = "slot3"
        
        self.scoreSlot32 = simpleGE.Label()
        self.scoreSlot32.center = (420 ,226)
        self.scoreSlot32.size = (200, 30)
        self.scoreSlot32.text = "slot3/2"
        #slot 4
        self.scoreSlot4 = simpleGE.Label()
        self.scoreSlot4.center = (220, 258)
        self.scoreSlot4.size = (200, 30)
        self.scoreSlot4.text = "slot4"
        
        self.scoreSlot42 = simpleGE.Label()
        self.scoreSlot42.center = (420 ,258)
        self.scoreSlot42.size = (200, 30)
        self.scoreSlot42.text = "slot4/2"
        #slot 5
        self.scoreSlot5 = simpleGE.Label()
        self.scoreSlot5.center = (220, 290)
        self.scoreSlot5.size = (200, 30)
        self.scoreSlot5.text = "slot5"
        
        self.scoreSlot52 = simpleGE.Label()
        self.scoreSlot52.center = (420 ,290)
        self.scoreSlot52.size = (200, 30)
        self.scoreSlot52.text = "slot5/2"
        
        
        
        # self.board = simpleGE.Label()
        # self.board .center = (320, 130)
        # self.board .size = (200, 30)
        # self.board .text = "Leaderboard"
        
        # self.board = simpleGE.Label()
        # self.board .center = (320, 130)
        # self.board .size = (200, 30)
        # self.board .text = "Leaderboard"
        
        # self.board = simpleGE.Label()
        # self.board .center = (320, 130)
        # self.board .size = (200, 30)
        # self.board .text = "Leaderboard"
        
        
        self.sprites = [
            self.lblScore,
            self.btnPlay,
            self.btnQuit,
            self.board,
            self.scoreSlot1,
            self.scoreSlot12,
            self.scoreSlot2,
            self.scoreSlot22,
            self.scoreSlot3,
            self.scoreSlot32,
            self.scoreSlot4,
            self.scoreSlot42,
            self.scoreSlot5,
            self.scoreSlot52,
            self.btnName
            ]
    
               
    def process(self):
        if self.btnPlay.clicked:
            self.status = "play"
            self.stop()
        if self.btnQuit.clicked:
            self.status = "quit"
            self.stop()
        if self.btnName.clicked:
            print("PLease enter you name ot initals:")
            self.playerName = input()
            # self.scoreAdder(self.playerName, self.score,Hscores)
    
    # def scoreAdder(self, playerName, score, Hscores):
        # self.scoreSlot1.text = self.playerName
        # self.scoreSlot12.text = self.score
        # file = open("previousScore.txt", "w")
        # file.write(f" {self.playerName}: {self.score}")
        # file.close()
        # print ("Previous score list has been updated")
        # Hscores = {hplayerName:hscore} 
        # insertAt = len(self.score_Hscores)
        # for i in range(len(self.score_Hscores)):
        #     self.scoreSlot[i].text = Hscores{hplayerName}
        #     self.scoreSlot[i]2.text = Hscores{hscore}
        
        
          
    def loadScores():
        fileName = "PreviousScore.json"
        inFile = open(fileName, "r")
        Hscores = json.load(inFile)
        inFile.close()
        return Hscores
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
             
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center = (500, 30)
        

class Soldier(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("SoldierUp.png")
        self.setSize(50, 50)
        self.position = (320,400)
        self.moveSpeed = 6
    
    
    def process(self):
        if self.isKeyPressed(pygame.K_a):
            self.imageAngle += 5
        if self.isKeyPressed(pygame.K_d):
            self.imageAngle -= 5
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += self.moveSpeed
            
        """ press X key for a stream of bullets """
        if self.scene.isKeyPressed(pygame.K_x):
             self.scene.currentBullet += 1
             if self.scene.currentBullet >= self.scene.NUM_BULLETS:
                 self.scene.currentBullet = 0
             self.scene.bullets[self.scene.currentBullet].fire()

class Bullet(simpleGE.Sprite):
    def __init__(self, scene, parent):
        super().__init__(scene)
        self.parent = parent
        self.colorRect("white",(5,5))
        self.setBoundAction(self.HIDE)
        self.hide()
        
    def fire(self):
        self.show()
        self.position = self.parent.position
        self.moveAngle = self.parent.imageAngle
        self.speed = 20
        
    
class numLives(simpleGE.Label):
     def __init__(self): 
         super().__init__()
         self.text = "Lives left: 5"
         self.center = (100,450)
     
    
class Zombie(simpleGE.Sprite):
    def __init__(self,scene):
        super().__init__(scene)               
        self.setImage("ZombieLeftX.png")
        self.setSize(100,100)
        self.reset()
        
    def reset(self):
        side = random.randint(0,3)
        if side == 0:
            # top            
            self.x = random.randint(0, self.screen.get_width())
            self.y = random.randint(40,60)
            self.dy += random.randint(1,3)
        elif side == 1:
            # left
            self.x = random.randint(0,480)
            self.y = random.randint(0, self.screen.get_height())
            self.dx += random.randint(2, 4)
        elif side == 2:
            # bottom
            self.x = random.randint(0, self.screen.get_width())
            self.y = random.randint(550, 600)
            self.dy += random.randint(-3, -1)
        else:
            # right
            self.x = random.randint(400, 440)
            self.y = random.randint(0, self.screen.get_height())
            self.dx -= random.randint(1, 3)
            
        
    # def checkBounds(self):
    #       if self.right > self.screenWidth:
    #           self.reset()
       
    #       elif self.left < self.screenWidth:
    #           self.reset()
        
    #       elif self.top > self.screenHeight:
    #           self.reset()
        
    #       elif self.bottom < self.screenHeight:
    #           self.reset()
        
        
              
    
        
        
      
def main():
    keepGoing = True
    score = 0
    
    while keepGoing:
        intro = Intro(score)
        intro.start()
        
        if intro.status == "quit":
            LeaderBoard = leaderBoard(score)
            LeaderBoard.start()
            if LeaderBoard.status =="quit":
                keepGoing = False
                
    
        else:
            game = Game()
            game.start()
            score = game.score

if __name__ == "__main__":
    main()
    