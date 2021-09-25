from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as pl
import netCDF4 as nc
print("Please enter model name such as 'CCSM4' 'NorESM1-ME' or CESM1-CAM5, ")
model = input("Enter the Historical model Name: ")
print("What type of plots you need")
typl = input("1: for climatologyy or 2: for Anomalies: ")
if int(typl)==1:
    tm1,  tm2 = (input("Enter the time period  between 1850 to 2005 :")).split()
else:
    tm1 = (input("Enter any year  between 1850 to 2005 :"))

lon11, lon21 = (input("Enter the Longitude between 0 to 360 :")).split()
lat11, lat21 = (input("Enter the latitude  between -90 to 90 :")).split()
lon1,lon2,lat1,lat2=float(lon11),float(lon21),float(lat11),float(lat21)
slt = int((lat2 - lat1)/5)
sln = int((lon2 - lon1)/10)
#lon1,lon2,lat1,lat2=0,360,-60,60
#plot gird setting======
if slt >= 10 :
    slt = 10
else:
    slt = 5
    
    
if sln >= 10 :
    sln = 20
else:
     sln = 10
        
#plot gird setting======    



#model='CESM1-CAM5'
trange='185001-200512'
fd=nc.Dataset('./data/pr_Amon_'+model+'_historical_r1i1p1_'+trange+'.nc')
fd1=nc.Dataset('./data/ts_Amon_'+model+'_historical_r1i1p1_'+trange+'.nc')
lon=fd.variables['lon'][:]
lat=fd.variables['lat'][:]
latmn = np.argmin(np.fabs(lat-lat1)).min()
latmx = np.argmin(np.fabs(lat-lat2)).min()
lonmn = np.argmin(np.fabs(lon-lon1)).min()
lonmx = np.argmin(np.fabs(lon-lon2)).min() 

# ---------Rainfall analysis 
pr=fd.variables['pr'][:,latmn:latmx,lonmn:lonmx]
pr=pr*86400
nt,ny,nx=pr.shape
prny,prnx=ny,nx
nyr=int(nt/12)
pr4d=np.reshape(pr,(nyr,12,ny,nx))
prtave=np.mean(pr4d[:,5:8,:,:],axis=1)
prclm=np.mean(prtave,axis=0)
pranom=prtave*0.0
for k in range(nyr):
    pranom[k,:,:]=prtave[k,:,:]-prclm

#=========Sea Surface temperature =============

ts=fd1.variables['ts'][:,latmn:latmx,lonmn:lonmx]
ts = ts - 273.15 
ts4d=np.reshape(ts,(nyr,12,ny,nx))
tstave=np.mean(ts4d[:,5:8,:,:],axis=1)
tsclm=np.mean(tstave,axis=0)
tsanom=tstave*0.0
for k in range(nyr):
    tsanom[k,:,:]=tstave[k,:,:]-tsclm

if int(typl)==1:
    ht1, ht2 = int(tm1),int(tm2)
    prtave1=prtave[int(ht1-1850):int(ht2-1850),:,:]
    tstave1=tstave[int(ht1-1850):int(ht2-1850),:,:]
    ccpr = np.mean(prtave1,axis=0)
    ccts = np.mean(tstave1,axis=0)
    prclbr = np.arange(1,30,3)
    tsclbr = np.arange(20,38,1)
    tstr = 'Climatology: '+tm1 + '-' +tm2
    
else:
    ht1 = int(tm1)
    ccpr=pranom[int(ht1-1850),:,:]
    ccts=tsanom[int(ht1-1850),:,:]
    prclbr = np.arange(-2,2,0.2)
    tsclbr = np.arange(-1,1,0.1)
    tstr = 'Anomaly: '+tm1 


#===========================plotting =================
fig, axes = pl.subplots(2, 1)

#axes[0].set_title("Rainfall")
m = Basemap(resolution='l',projection='mill',lon_0=(lonmn+lonmx)/2.0,llcrnrlon=lon1,llcrnrlat=lat1,urcrnrlon=lon2,urcrnrlat=lat2,ax=axes[0])
lons, lats = np.meshgrid(lon[lonmn:lonmx],lat[latmn:latmx])
x,y=m(lons,lats)
#cc = np.mean(pranom,axis=0) #anomalies plot====
axes[0].get_xaxis().set_visible(True)
cs1=m.contourf(x,y,ccpr,cmap=pl.cm.coolwarm,animated=True)
m.drawcoastlines(color='black', linewidth=0.4)
m.drawmapboundary(fill_color='grey')
m.drawparallels(np.arange(lat1,lat2,slt),labels=[1,0,0,0])
m.drawmeridians(np.arange(lon1,lon2,sln),labels=[0,0,1,0])
cbar=m.colorbar(cs1,location='right')
cbar.set_label(' Rainfall(mm/day)')

#axes[1].set_title("SST")
m1 = Basemap(resolution='l',projection='mill',lon_0=(lonmn+lonmx)/2.0,llcrnrlon=lon1,llcrnrlat=lat1,urcrnrlon=lon2,urcrnrlat=lat2,ax=axes[1])

cs2=m1.contourf(x,y,ccts,cmap=pl.cm.coolwarm,animated=True)
m1.drawcoastlines(color='black', linewidth=0.4)
m1.drawmapboundary(fill_color='grey')
m1.drawparallels(np.arange(lat1,lat2,slt),labels=[1,0,0,0])
m1.drawmeridians(np.arange(lon1,lon2,sln),labels=[0,0,1,0])
#pl.contourf(prlon[prx0:prx1],prlat[pry0:pry1],cc,20)
cbar1=m1.colorbar(cs2,location='right')
cbar1.set_label(' Temperature(degC)')
fig.suptitle(tstr, fontsize=12)
fig.tight_layout()
pl.show()