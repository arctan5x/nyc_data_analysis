import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import time

'''
Plotting functions are from tutorials at https://towardsdatascience.com/mapping-geograph-data-in-python-610a963d2d7f
Shapefiles are from https://geo.nyu.edu/catalog/nyu-2451-36743
'''

sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10,6))

shp_path = "nyc_taxi_zones/taxi_zones.shp"
sf = shp.Reader(shp_path)

print len(sf.shapes())

print sf.records()[1]

def read_shapefile(sf):
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

df = read_shapefile(sf)
print df.shape
print df.sample(5)

def plot_shape(id, s=None):
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon,y_lat) 
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    return x0, y0

def plot_map(sf, x_lim = None, y_lim = None, figsize = (11,9)):
    plt.figure(figsize=figsize)
    id = 0
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')
        
        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, id, fontsize=5)
        id = id+1
    
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)

def plot_map_fill(pickup_ids, dropoff_ids, sf, x_lim = None, y_lim = None, figsize = (11,9)):
    plt.figure(figsize = figsize)
    fig, ax = plt.subplots(figsize = figsize)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')
    
    for i in pickup_ids:
        shape_ex = sf.shape(i-1)
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        ax.fill(x_lon,y_lat, 'r')

    for i in dropoff_ids:
        shape_ex = sf.shape(i-1)
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        if i in pickup_ids:
            ax.fill(x_lon,y_lat, 'yellow')
        else:
            ax.fill(x_lon,y_lat, 'b')
    
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)
# plot_map(sf)
# Green morning 
# plot_map_fill([255, 7, 82, 41, 129], [129, 7, 82, 223, 42], sf)
# Green evening
# plot_map_fill([255, 7, 82, 41, 129], [129, 7, 82, 42, 112], sf)
# Yello morning
# plot_map_fill([79, 230, 48, 249, 132], [79, 48, 170, 68, 107], sf)
# Yellow evening
plot_map_fill([79, 230, 48, 249, 148], [79, 48, 170, 68, 186], sf)


plt.show()
