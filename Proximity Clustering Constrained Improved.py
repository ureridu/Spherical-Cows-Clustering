# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:45:14 2017

@author: SKowalski
"""
import timeit

#print(timeit.timeit(r'''

from tree_sort import BST
import pandas
import numpy
import scipy
from scipy import spatial
from geopy.distance import vincenty
import operator
import datetime
from operator import itemgetter
import os


min_in_cluster = 1
max_in_cluster = 21
unique_in_cluster = 1
radius = 100

timer_start = datetime.datetime.now()
prev_time = timer_start

path = os.getcwd()

#stores_in = pandas.read_excel(path + 'Walmart Stores.xlsx')
stores_in = pandas.read_excel(path + '/Shark THing.xlsx')

with open(path + '/2015_Gaz_zcta_national.txt', 'r') as infile:
    zips = infile.read()

    #*GEOID, ALAND, AWATER, ALAND_SQMI, AWATER_SQMI, INTPTLAT, INTPTLONG = infile.read().split(' ')
zips = zips.split('\n')
clean = []
for row in zips:
    cols = [x.strip() for x in row.split('\t')]
    clean.append(cols)

del clean[0]

all_zip_in = pandas.DataFrame(clean)
all_zip_in.columns = ['Zip', 'Aland', 'Awater', 'AlandSQMI', 'AwaterSQMI', 'Lat', 'Long']
all_zip_in = all_zip_in[all_zip_in.Lat.notnull()]
del zips
del clean

reference = (0, 0)
#all_zip = all_zip_in[['Zip', 'Lat', 'Long']]
#all_zip['Lat'] = [vincenty((x.Lat, 0), reference).miles for x in all_zip.itertuples()]
#all_zip['Long'] = [vincenty((0, x.Long), reference).miles for x in all_zip.itertuples()]
#
#stores = stores_in[['Store Number', 'Lat', 'Long']]
#stores['Lat'] = [vincenty((0, x.Lat), reference).miles for x in stores.itertuples()]
#stores['Long'] = [vincenty((0, x.Long), reference).miles for x in stores.itertuples()]

all_zip = all_zip_in[['Zip', 'Lat', 'Long']]
for row in all_zip.itertuples():
    i = row.Index
    all_zip.set_value(i, 'Lat', vincenty((row.Lat, 0), reference).miles)
    all_zip.set_value(i, 'Long', vincenty((0, row.Long), reference).miles)


stores = stores_in[['Store Number', 'Lat', 'Long']]
for row in stores.itertuples():
    i = row.Index
    stores.set_value(i, 'Lat', vincenty((row.Lat, 0), reference).miles)
    stores.set_value(i, 'Long', vincenty((0, row.Long), reference).miles)

zip_coords = all_zip.as_matrix(columns=['Lat', 'Long'])
store_coords = stores.as_matrix(columns=['Lat', 'Long'])

dist_mat = pandas.DataFrame(spatial.distance.cdist(zip_coords, store_coords), columns=stores['Store Number'])

cur_time = datetime.datetime.now()
print('\nDistance Matrix Complete', cur_time - prev_time)
prev_time = cur_time

cluster_list = []
clust_set = set()
for row in dist_mat.iterrows():
    i=row[0]
    r = row[1]
    r_index = r.index
    
    r.reset_index(inplace=True, drop=True)
    to_row = numpy.where(r <= radius)[0]
    
    
#    to_sort = zip(r, r.index)
    to_sort = zip(r[to_row], r_index[to_row])
    sorted_row = sorted(to_sort, key=lambda x: x[0])
    
#    ig = itemgetter(0)
#    sorted_row = sorted(to_sort, key=ig)
#    
##    r.reset_index(inplace=True, drop=True)
##    sort_order = numpy.argsort(r)
##    sorted_row = r[sort_order]
##    sorted_index = r_index[sort_order]
#    
    interim_clust = sorted_row[:max_in_cluster]
#    clust = [ind for dist, ind in interim_clust if dist <= radius]
    clust = [ind for dist, ind in interim_clust]
##    clust = [sorted_index[i] for i, x in enumerate(sorted_row) if x <= radius]
    if len(clust) >= min_in_cluster:
        cluster_list.append([all_zip.get_value(i, 'Zip'), clust, 0])
        clust_set.update(clust)


cur_time = datetime.datetime.now()
print('\nForced Clustering Complete', cur_time - prev_time)
prev_time = cur_time

clust_dict = {x: 0 for x in clust_set}
all_stores = set(stores['Store Number'])
clust_lookup = {store: [] for store in all_stores}

for i, row in enumerate(cluster_list):
    for store in row[1]:
        clust_dict[store] += 1
        clust_lookup[store].append(i)

clust_sums = {x[0]: 0 for x in cluster_list}

cur_time = datetime.datetime.now()
print('\nPrep Work Complete', cur_time - prev_time)
prev_time = cur_time

cluster_list = pandas.DataFrame(cluster_list, columns=['Cluster', 'Items', 'Uniqueness'])
cluster_list.set_index('Cluster', inplace=True, drop=True)

protected = set()
to_update = list(cluster_list.index)
run = 1
while run:
    run = None
    for clust in to_update:
        stores, _ = cluster_list.loc[clust, :]
        sums = 0
        unique_stores = 0
        for store in stores:
            sums += clust_dict[store]
            if clust_dict[store] == 1:
                unique_stores += 1

        if unique_stores >= unique_in_cluster:
            protected.add(clust)
        cluster_list.set_value(clust, 'Uniqueness', sums/(len(clust[1])))

#    cluster_list.sort_values('Uniqueness', ascending=False, inplace=True)
        
    clust_tree = BST(list(cluster_list['Uniqueness']), list(cluster_list.index))
    sorted_list = reversed(clust_tree.listify())
    print('sorted')

    to_update = set()
    altered_stores = set([])
    num_del = 0
    for item in sorted_list:
        row = cluster_list.loc[item.name]
#    for i, clust in enumerate(cluster_list):
        if item.name not in protected and not any(x in altered_stores for x in row.Items):
            run = 1
            for store in row.Items:
                clust_dict[store] -= 1
                altered_stores.add(store)
                clust_lookup[store].remove(i)
                to_update.update(clust_lookup[store])
                
#            ind = (i + 1 - num_del) * (-1)
#            ind = i
#            print(i, ind, clust[0], cluster_list[ind][0])
            cluster_list.drop(item.name, inplace=True)
            clust_tree.snip_node(clust_tree.node_ref[row.Cluster])
            num_del += 1
            break
    to_update = [int(x) for x in to_update]
    break
count = 0
count_included = 0
dup = 0
for key, val in clust_dict.items():
    count += 1
    if val > 0:
        count_included += 1
        if val > 1:
            dup = 1


cur_time = datetime.datetime.now()
print('\nPairing Complete', cur_time - prev_time)
print('Finished', cur_time - timer_start)

print(len(all_stores), count_included, int((count_included/count)*100), dup)
print(len(cluster_list), int(count_included/len(cluster_list)) )

#''', number = 3))

    