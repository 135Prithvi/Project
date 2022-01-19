from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import (NumericProperty , ReferenceListProperty, ObjectProperty, ListProperty)
from random import randint
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.config import Config
                                                        
# Setting size to resizable
Config.set('graphics','width', 700)
Config.set('graphics','height', 700)
Config.write()

class Paddle(Widget):
    score = NumericProperty(0)
    
    def bounceBall(self ,ball):
        
        if self.collide_widget(ball):
            vx ,vy = ball.velocity
            offset = (ball.center_y - self.center_y) /(self.height /2)
            bounced = Vector(-1* vx, vy)
            vel = bounced * 1.001
            ball.velocity = vel.x ,vel.y + offset 
        
        


class PongBall(Widget):
    
    velocityX = NumericProperty(0)
    velocityY = NumericProperty(0)
    velocity = ReferenceListProperty(velocityX, velocityY)
    color = ListProperty((1,1,1,1))
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    

    def serveBall(self ,vel=(5,0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(5,0).rotate(randint(0,45))
        
        
    
    def update(self , dt ):
        
        self.ball.move()
        self.ball.color=(1,0,0,1)
        self.player1.y = self.ball.y
        self.player1.bounceBall(self.ball)
        self.player2.bounceBall(self.ball)
        
        

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocityY *= -1
            
            
            
        #if (self.ball.x < 0) or (self.ball.right > self.width):
            #self.ball.velocityX *= -1
    

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serveBall(vel=(5,0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serveBall(vel=(-5,0))

        if  self.player2.score>=10:
            self.player1.score = 0
            self.player2.score = 0
            self.serveBall(vel=(5,0))
            #self.ids.comment.text = "You Win"
            
        if self.player1.score>=10 :
            self.player1.score = 0
            self.player2.score = 0
            self.serveBall(vel=(5,0))
            #self.ids.comment.text = "You Loose"
            
        
        
        

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        
        if keycode[1] == 'up':
            self.player2.center_y += 25
        elif keycode[1] == 'down':
            self.player2.center_y -= 25
        return True
            
            
       
        
    def on_touch_move(self, touch):
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y



class PongApp(App):
    def build(self):
        #Window.clearcolor = (0,1,0,1)
        game = PongGame()
        game.serveBall()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game
    
PongApp().run()
