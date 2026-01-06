import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Box:
   def __init__(self, x: float, y: float):
       self.x = x
       self.y = y

   def rotate(self):
       x_tmp = self.x
       y_tmp = self.y
       self.x = y_tmp
       self.y = x_tmp


class BoxLocation(Box):
   def __init__(self, x: float, y: float, coords: np.ndarray):
       super().__init__(x, y)
       self.coords = coords


   def translate(self, vec: np.ndarray):
       if vec.size != self.coords.size:
           raise ValueError('translation vector does not match coordinates')
       self.coords += vec


class BoxDisp:
   def __init__(self, box_list: list[BoxLocation]):
       self.card = len(box_list)
       self.box_list = box_list

class Container:
   def __init__(self, length, width):
       self.width = width 
       self.length = length