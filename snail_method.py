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
    def __init__(self, length: float, width:float):
        self.width = width 
        self.length = length

    def fit(self, box:Box, n_hor:int):
        '''
        Uses the Snail Method to compute a particular (namely, with a fixed number of horizontal boxes) disposition of
        boxes into a container.
        :param box: box object to fit into the container
        :param n_hor: number of horizontal boxes layers
        :return: list of BoxDisp object.
        '''
        if box.x < box.y:
            box.rotate()


        box_disp_list = []


        container_areas = [
            {'n_col': n_hor,
                'n_row': self.length // box.y,
                'start': np.array([0, 0])},
            {'n_col': (self.width - n_hor * box.x) // box.y,
                'n_row': self.length // box.x,
                'start': np.array([n_hor * box.x, 0])},
            {'n_col': (self.width - n_hor * box.x) // box.x,
                'n_row': (self.length % box.x) // box.y,
                'start': np.array([n_hor * box.x, self.length - self.length % box.x])}
        ]


        for area in container_areas:

            x_coords = area['start'][0] + box.x * np.arange(stop = area['n_col'])
            y_coords = area['start'][1] + box.y * np.arange(stop = area['n_row'])


            if x_coords.size * y_coords.size > 0:
                #grid_x, grid_y = np.meshgrid(x_coords, y_coords, sparse=True)   # grid
                for vec in np.array(np.meshgrid(x_coords, y_coords)).T.reshape(-1, 2):
                    box_disp_list.append(BoxLocation(box.x, box.y, vec))


            box.rotate()


        box_disp = BoxDisp(box_disp_list)


        return box_disp


    def compute_disp(self, box: Box):
        '''
        Prepares the correct inputs for the container.fit method of boxes in the container and checks whether the max number
        of boxes into the container is reached.
        :param box: box object to display into the container
        :return: list of dictionaries with very proper boxes disposition in the container and the associated number of
        boxes.
        '''
        if box.x < box.y:
            box.rotate()


        max_hor_col = int(self.width // box.x)


        sur_box = box.x * box.y; sur_container = self.width * self.length
        th_lim = sur_container // sur_box


        disp_list = []


        for n_hor in range(max_hor_col + 1):
            disp_tmp = self.fit(box, n_hor)
            disp_list.append(disp_tmp)


            if disp_tmp.card > th_lim:
                raise ValueError('theoretical limit has been passed')
            elif disp_tmp.card == th_lim:
                print('theoretical limit has been reached')
                break


        return disp_list

    # TODO: qui va aggiunta la corretta gestione del limite teorico.
    def optimize(self, box: Box):
        '''
        Finds the optimal displacement of boxes in a container.
        :param box: box object to display into the container
        :return: the optimal BoxDisp object.
        '''

        disp_list = self.compute_disp(box)


        opt_disp = BoxDisp([])


        for disp in disp_list:
            if disp.card > opt_disp.card:
                opt_disp = disp


        return opt_disp