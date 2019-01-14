"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        print(self)
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie 

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col)) 
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        if entity_type == HUMAN:
            entities = self._human_list
        else:
            entities = self._zombie_list
            
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
     
        distance_field = [[self._grid_width * self._grid_height for dummy_col in range(self._grid_width)] 
                          for dummy_row in range(self._grid_height)]
        # Create queue boundary
        boundary = poc_queue.Queue()
        # Copy either zombie list or humanlist
        for entity in entities:
            boundary.enqueue(entity)
            # For cells in the queue initialize visited to be FULL
            visited.set_full(entity[0],entity[1])
            # For cells in the queue initialize 
            distance_field[entity[0]][entity[1]] = 0
            
        # while boundary is not empty
        while len(boundary) > 0:
            # current <- dequeue boundary
            curr_cell = boundary.dequeue()
            neighbor_cells = self.four_neighbors(curr_cell[0], curr_cell[1])
            # for all neighbor_cell of current_cell:
            for neighbor in neighbor_cells:
                # if neighbor cell is not in visited
                if visited.is_empty(neighbor[0],neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    # add neighbor_cell to visited
                    visited.set_full(neighbor[0],neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[curr_cell[0]][curr_cell[1]] + 1
            
        
        return distance_field
        
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
     
        new_location = []
        
        for human in self._human_list:
            locations = self.eight_neighbors(human[0], human[1])
            curr_dist = zombie_distance_field[human[0]][human[1]]
           
            # get highest max distance
            max_dist = max([zombie_distance_field[loc[0]][loc[1]] for loc in locations 
                                if self.is_empty(loc[0],loc[1])])
            
            # get locations that match max distance
            if max_dist > curr_dist:
                max_locations = [loc for loc in locations if self.is_empty(loc[0],loc[1]) and 
                             zombie_distance_field[loc[0]][loc[1]] == max_dist]
            
                # update new location for human
                new_location.append(random.choice(max_locations))
            else:
                new_location.append((human[0],human[1]))
        self._human_list = new_location 
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_location = []
        
        for zombie in self._zombie_list:
            locations = self.four_neighbors(zombie[0], zombie[1])
            curr_dist = human_distance_field[zombie[0]][zombie[1]]
            
            try:
                # get lowest distance
                min_dist = min([human_distance_field[loc[0]][loc[1]] for loc in locations
                                if self.is_empty(loc[0],loc[1])])
            except(ValueError):
                new_location.append((zombie[0],zombie[1]))
                continue
            # get locations that match lowest distance
            if min_dist < curr_dist:
                min_locations = [loc for loc in locations if self.is_empty(loc[0],loc[1]) and
                                 human_distance_field[loc[0]][loc[1]] == min_dist]
                
                # update new location for human
                new_location.append(random.choice(min_locations))
            else:
                new_location.append((zombie[0],zombie[1]))
        self._zombie_list = new_location    
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Apocalypse(30, 40))
#poc_zombie_gui.run_gui(Apocalypse(3, 3, [(0, 1), (1, 2), (2, 1)], [(0, 2)], [(1, 1)]))
