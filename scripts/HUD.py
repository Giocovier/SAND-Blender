import bge
#import bpy
import GameLogic
import math
from Logging import Logging
    
class HUD(object):
    '''
    this class is the HUD
    '''
    def __init__(self,cont):
        self.cont = cont
        self.own = cont.owner
        self.log = Logging("HUD","Debug")
        self.scene = bge.logic.getCurrentScene()
        self.enemyStatus = self.scene.objects["EnemyStatus"]
        self.ammoStatus = self.scene.objects["AmmoStatus"]
        self.clipStatus = self.scene.objects["ClipStatus"]
        self.goActuator = self.own.actuators["GameOverAct"]
        self.suspMainAct = self.own.actuators["SuspMain"]
        self.suspHUDAct = self.own.actuators["SuspHUD"]
        self.scoreStatus = self.scene.objects["ScoreStatus"]
        self.timer = self.scene.objects["Timer"]
        
        self.msgSensor = self.cont.sensors["HUDMessage"]
        self.enemyCount = 0
        self.ammoCount = 0
        self.clipCount = 0
        self.score = 0
        self.enemyHit = 0
        self.enemy(0)
        self.ammo(0)
        self.clips(0)
        self.log.msg("Init complete.")
        
    def update(self):
        self._handleMessage()
        self.calcScore()
        
    def _handleMessage(self):
        '''
        separate out the message bodies and process them to update the HUD
        '''

        if self.msgSensor.positive :  
            for subject in self.msgSensor.subjects:
                f = None
                try:
                    f = getattr(self,subject.lower())
                except AttributeError:
                    pass
                
                if f:
                    f(self.msgSensor.bodies[self.msgSensor.subjects.index(subject)])
                else:
                    #self.log.msg("Missing function for %s"%(subject))
                    pass

            
    def ammo(self,msg):
        self.ammoCount = int(msg)
        self.ammoStatus.text = "Ammo: "+str(self.ammoCount)
        
    def gameover(self,msg):
            self.controller = GameLogic.getCurrentController()
            self.controller.activate(self.suspMainAct)
            self.controller.activate(self.suspHUDAct)
            self.controller.activate(self.goActuator)
            
        
    def clips(self,msg):
        self.clipCount = int(msg)
        self.clipStatus.text = "Clips: "+str(self.clipCount)
    
    def calcScore(self): 
        try:
            time = float(self.timer.text) if float(self.timer.text)>0 else 1
            self.score =  math.floor((self.enemyHit/time)*100)
            self.scoreStatus.text = "Score: "+str(self.score)
            

        except Exception as e:
            pass
        
    def enemy(self,msg):
        if int(msg) == -1:
            #self.log.msg(msg)
            self.enemyHit +=1
            
        self.enemyCount = self.enemyCount + int(msg)
        self.enemyStatus.text = "Enemy: "+str(self.enemyCount)
    
def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
    
    if 'matrix.hud' not in own:
        own['matrix.hud'] = HUD(cont)
    else:
        own['matrix.hud'].update()

if bge.logic.getCurrentController().mode == 0:
    main() 