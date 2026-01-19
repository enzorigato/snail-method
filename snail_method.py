import numpy as np
from matplotlib.figure import Figure
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

    def show(self, plt_width, plt_length) -> Figure:
        '''
        Plots the displacement of a specific disposition of boxes in a container.
        :param plt_width: width of the container containing the boxes
        :param plt_length: length of the container containing the boxes
        :return: figure object.
        '''
        fig, ax = plt.subplots()

        ax.axis('scaled')
        ax.set(xlim=(0, plt_width), ylim = (0, plt_length))

        for box_loc in self.box_list:
            p = patches.Rectangle(tuple(coord for coord in box_loc.coords),
                                        box_loc.x, box_loc.y,
                                        color='r',
                                        fill=False)
            ax.add_patch(p)

        return fig

class Container:
    def __init__(self, length: float, width:float):
        self.width = width 
        self.length = length

    def fit(self, box:Box, n_hor:int) -> BoxDisp:
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

        # this contains the theoretical info, such as the number of boxes, in order to place them by area (vertical, horizontal, eps-area) 
        # given the particular number of horizontal boxes one wants.
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


        for area in container_areas: # iterate along the areas of the container.

            x_coords = area['start'][0] + box.x * np.arange(area['n_col'])
            y_coords = area['start'][1] + box.y * np.arange(area['n_row'])


            # case in which there exists at least one box in the current area for such a configuration. 
            if x_coords.size * y_coords.size > 0:
                #grid_x, grid_y = np.meshgrid(x_coords, y_coords, sparse=True)   # grid
                for vec in np.array(np.meshgrid(x_coords, y_coords)).T.reshape(-1, 2):
                    box_disp_list.append(BoxLocation(box.x, box.y, vec))


            box.rotate()


        box_disp = BoxDisp(box_disp_list)


        return box_disp


    def compute_disp(self, box: Box) -> list[BoxDisp]:
        '''
        Computes all the possible dispositions of boxes into a container using the snail method. Snail method stops ifa surface comparison states that a theoretical limit has been reached.
        :param box: box object to display into the container
        :return: list of BoxDisp, namely the eligible dispositions of boxes in the container
        '''
        if box.x < box.y:
            box.rotate()


        max_hor_col = int(self.width // box.x)


        sur_box = box.x * box.y; sur_container = self.width * self.length
        th_lim = sur_container // sur_box


        disp_list = []

        # every eligible disposition in snail method is parametrized by the number of horizontal columns.
        # Varying this parameter produces all the eligible disposition, which are stored in a list. 
        for n_hor in range(max_hor_col + 1):
            disp_tmp = self.fit(box, n_hor)
            disp_list.append(disp_tmp)


            if disp_tmp.card > th_lim:
                raise ValueError('theoretical limit has been passed')
            elif disp_tmp.card == th_lim:
                break


        return disp_list

    # TODO: qui va aggiunta la corretta gestione del limite teorico.
    def optimize(self, box: Box) -> BoxDisp:
        '''
        Finds the optimal displacement of boxes in a container among the possible ones.
        :param box: box object to display into the container
        :return: the optimal BoxDisp object.
        '''
        # computation of the eligible dispositions
        disp_list = self.compute_disp(box) 


        opt_disp = BoxDisp([])

        # monkey list comprehension of the BoxDisp list in order to find the max (this part needs to be optimized) 
        for disp in disp_list:
            if disp.card > opt_disp.card:
                opt_disp = disp 


        return opt_disp
    

    # tests.

if __name__ == '__main__':
    container = Container(80, 120)
    box = Box(60, 60)


    opt = container.optimize(box)


    opt.show(container.width, container.length)


    plt.show()
