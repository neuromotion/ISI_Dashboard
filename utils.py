# utility functions used accross the project

def dictCollect(l_ds,key):
    """for each dict in the list l_ds, collect the values accessed by key into a list"""
    lst = []
    for d in l_ds: 
        lst.extend(d[key])
    return lst
