#!/usr/bin/env python

import pandas as pd
import numpy as np
import cartopy.crs as ccrs
# need following two lines or else it segfaults
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy
import sys
import pickle

# %matplotlib inline

# got data from https://nrcs.app.box.com/v/huc
import cartopy.io.shapereader as shpreader

# %%

hucnum = sys.argv[1]
state = sys.argv[2]

# shpfilename = 'hu2.shp'
if int(hucnum) < 10:
    shpfilename = 'hu' + str(hucnum) + '/hu' + str(hucnum) + '.shp'
else:
    shpfilename = 'hu' + str(hucnum) + '/' + state + '_' + str(hucnum) + '.shp'

print('Loading', shpfilename)
reader = shpreader.Reader(shpfilename)
# %%

# get state watersheds
allgeom = []
for record, geom in zip(reader.records(), reader.geometries()):
    if state in record.attributes['STATES']:
        # print(record.attributes['NAME'])
        allgeom.append(geom)

print(len(allgeom), 'HUCs containing', state)

# %%
if hucnum == '2':
    extlon0 = []
    extlat0 = []
    extlon1 = []
    extlat1 = []
    for g in allgeom:
        extlon0.append(g.bounds[0])
        extlat0.append(g.bounds[1])
        extlon1.append(g.bounds[2])
        extlat1.append(g.bounds[3])

    lonrng = np.max(extlon1) - np.min(extlon0)
    latrng = np.max(extlat1) - np.min(extlat0)
    buf = 0.00
    lons = [np.min(extlon0) - buf*lonrng, np.max(extlon1) + buf*lonrng]
    lats = [np.min(extlat0) - buf*latrng, np.max(extlat1) + buf*latrng]
    if state == 'AK':
        lonlat = [lons[0]-20, lons[1]-20, lats[0], lats[1]]
    else:
        lonlat = [lons[0], lons[1], lats[0], lats[1]]
    print(lonlat)

    with open('lims/' + state + '.p', 'wb') as fp:
        pickle.dump(lonlat, fp)

with open('lims/' + state + '.p', 'rb') as fp:
    lonlat = pickle.load(fp)
# %%
fig = plt.figure(figsize=(10,8))

lons = [lonlat[0], lonlat[1]]
lats = [lonlat[2], lonlat[3]]
print(lonlat)

#if state == 'CA':
    #lons = [-125.24458573729996, -107.44075619769998]
    #lats = [29.377712395120042, 53.34149571288005]
#if state == 'WA':
    #lons = [-125.20499865915995, -109.45969718283995]
    #lats = [40.89276961990004, 53.11571027710005]
#if state == 'ME':
    #lons = [-93.75776785581996, -65.47484441717995]
    #lats = [40.22212215096006, 49.195173565040065]
#if state == 'NH':
    #lons = [-93.75776785581996, -65.47484441717995]
    #lats = [40.22212215096006, 49.195173565040065]
# if state == 'CA':
#     lons = [-124, -108]
#     lats = [28, 54]
# if state == 'ME':
#     lons = [-80, -66]
#     lats = [42, 49]
# if state == 'WA':
#     lons = [-126, -110]
#     lats = [40, 53]

#projection=ccrs.AlbersEqualArea(central_longitude=np.mean(lons),
#			        central_latitude=np.mean(lats),
#                                standard_parallels=lats)

projection=ccrs.Mercator()
ax = fig.add_subplot(1, 1, 1,
                     projection=projection)
ax.set_extent([lons[0], 0, lats[0], lats[1]],
              crs=ccrs.PlateCarree())
              #crs=projection)
ax.background_patch.set_visible(False)
ax.outline_patch.set_visible(False)
ax.add_geometries(allgeom, ccrs.PlateCarree(),
                  edgecolor='lightblue', facecolor='none', lw=.5)
#ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True)
# for geom in allgeom:
#     ax.add_geometries(geom, ccrs.PlateCarree(),
#                       edgecolor='lightblue', facecolor='none', lw=.5)
plt.savefig('hucmap_' + state + '_huc' + '%02d' % int(hucnum) + '.png', bbox_inches='tight', dpi=300)
# plt.savefig('hucmap_' + state + '_huc' + '%02d' % int(hucnum) + '.pdf', bbox_inches='tight')
print('Done')
# plt.show()
