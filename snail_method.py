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
            raise ValueError('translation vector does not match coordinates.')
        self.coords += vec


class BoxDisp:
    def __init__(self, n_hor: int, card: int | None = None, box_list: list[BoxLocation] | None = None):
        if (card is None) == (box_list is None):
            raise ValueError("Exactely one parameter between card or box_list has to be provided.")
        self.n_hor = n_hor
        self.card = len(box_list) if box_list is not None else card
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

        for box_loc in self.box_list if self.box_list is not None else []:
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

    def simulate(self, box: Box) -> list[BoxDisp]:
        '''
        Computes the cardinality of the possible dispositions, based on n_hor without placing the boxes in the container.
        :param self: container object
        :param box: box object to be placed into the container
        :return: list of BoxDisp which will only contain the n_horiz and how many boxes container contains
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

            container_areas = [
                {'n_col': n_hor,
                'n_row': self.length // box.y},
                {'n_col': (self.width - n_hor * box.x) // box.y,
                'n_row': self.length // box.x},
                {'n_col': (self.width - n_hor * box.x) // box.x,
                'n_row': (self.length % box.x) // box.y}
            ]

            card = int(np.sum(np.array([area['n_col'] * area['n_row'] for area in container_areas])))
            disp_list.append(BoxDisp(n_hor=n_hor, card=card))

            if card > th_lim:
                raise ValueError('theoretical limit has been passed')
            elif card == th_lim:
                break

        return disp_list

    def fit(self, box:Box, n_hor:int) -> BoxDisp:
        '''
        Uses the Snail Method to place in terms of coordinates a particular (namely, with a fixed number of horizontal boxes) disposition of
        boxes into a container.
        :param box: box object to fit into the container
        :param n_hor: number of horizontal boxes layers
        :return: list of BoxDisp object with the boxes placed into the container.
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
                #grid_x, grid_y = np.meshgrid(x_coords, y_coords, sparse=True)
                for vec in np.array(np.meshgrid(x_coords, y_coords)).T.reshape(-1, 2):
                    box_disp_list.append(BoxLocation(box.x, box.y, vec))


            box.rotate()

        box_disp = BoxDisp(n_hor, box_list=box_disp_list)

        return box_disp


    # TODO: qui va aggiunta la corretta gestione del limite teorico.
    def optimize(self, box: Box) -> BoxDisp:
        '''
        Finds the optimal displacement of boxes in a container among the possible ones.
        :param box: box object to display into the container
        :return: the optimal BoxDisp object.
        '''
        # computation of the eligible dispositions
        disp_list = self.simulate(box) # list of BoxDisp containing card per eligible n_hor
        opt = 0

        # monkey list comprehension of the BoxDisp list in order to find the max (this part should be optimized) 
        for disp in disp_list:
            if disp.card is not None and disp.card > opt:
                opt = disp.card
                opt_disp = disp

        if opt > 0:
            opt_fit = self.fit(box, opt_disp.n_hor) # produces the optimal configurations in terms of location
        else:
            raise ValueError('Box cannot fit into the container.')
        return opt_fit

    # tests.

if __name__ == '__main__':
    container = Container(80, 120)
    box = Box(87, 2)


    opt = container.optimize(box)


    opt.show(container.width, container.length)


    plt.show()
