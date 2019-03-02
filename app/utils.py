import numpy as np

# done
def direction_to_vector(direction):
    # convert a direction to a vector
    foo = {'up': (1, 0),
           'down': (-1, 0),
           'left': (0, -1),
           'right': (0, 1)
           }
    return(foo[direction])


def get_surrounding_coords(x_coord, y_coord):
    # given an (x,y) coordinate, get all surrounding
    up_new = (x_coord, y_coord+1)
    down_new = (x_coord, y_coord-1)
    left_new = (x_coord-1, y_coord)
    right_new = (x_coord+1, y_coord)
    return([up_new, down_new, left_new, right_new])


# done
def keywithmaxval(d):
    """ a) create a list of the dict's keys and values;
    b) return the key with the max value"""
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]
