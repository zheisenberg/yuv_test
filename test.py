# -*- coding: utf-8 -*-

from PIL import Image
import sys
from struct import *
import array
from numpy import *
set_printoptions(threshold=nan)
#this only works for 8 bit yuv format
def get_frame(videoname,dims):
#count the frame number of fuv file
    Ysiz = prod((144, 176))

    UVsiz = Ysiz / 4
    frelem = Ysiz + 2*UVsiz
    fid = open(videoname,'rb') #'tulips_yuv420_qcif.yuv','rb'
    fid.seek(0, 2)
    yuvbytes = fid.tell()
    print "the file size you are converting is", yuvbytes
    frames = floor(yuvbytes / frelem)
    fid.close()
    return frames

#this only works for one dimension
def fread(fid, nelements, dtype):
     dt = dtype #this is default as uint8, np.uint8

     data_array = fromfile(fid, dt, nelements)
     data_array.shape = (nelements, 1)

     return data_array

def fuv_read(videoname,dims,numfrm,startfrm):
    fp=open(videoname,'rb')  
    blk_size = prod(dims) *3/2 # 5/4 and 3/2, difference? 
    fp.seek(blk_size*startfrm,0)   # this stratfrm is 0, thus the above makes no diff, but again how to select number?
    Y=[]  
    U=[]  
    V=[]  
    UV=[]
#    print dims[0]  
#    print dims[1]  
    d00=dims[0]//2  
    d01=dims[1]//2  
#    print d00  
#    print d01  
    Yt=zeros((dims[0],dims[1]),uint8,'C')  
    Ut=zeros((d00,d01),uint8,'C')  
    Vt=zeros((d00,d01),uint8,'C')  

#    fp2 = open('test','wb+')
    for i in range(numfrm):
        for m in range(dims[0]):  
            for n in range(dims[1]):  
                #print m,n  
		#print type(fp.read(1))
                Yt[m,n]=ord(fp.read(1))  
        for m in range(d00):  
            for n in range(d01):  
                Ut[m,n]=ord(fp.read(1)) 
		Vt[m,n]=ord(fp.read(1))  
	Y=Y+[Yt]  
	U=U+[Ut]  
        V=V+[Vt] 

    fp.close()
    return (Y,U,V)	


def i420tonv12(i420_data,dims,numfrm,output):
    '''
    yyyy yyyy
    uu
    vv
    ->
    yyyy yyyy
    uv    uv
    ''' 
    fp2 = open(output,'wb')
    #dims = (144,176)
    Y,U,V = i420_data
###the sturcture for nv12 reshaping UV is skipped, since we finally are going to write into binary, then the order doesnot matter
#    UV = []
#    count = 1
    for i in range(numfrm):
        for j in range(dims[0]):
            for k in Y[i][j]:
                fp2.write(chr(k))
        for l in range(dims[0]//2):
            for m,n in zip(U[i][l], V[i][l]):
#                print "U [{}] is {}".format(l,m)
#                print "V [{}] is {}".format(l,n)
#                UV.append(m)
#                UV.append(n)
                fp2.write(chr(m))
                fp2.write(chr(n))
#                count = count + 1

            
###select your order####            
#            for m in U[i][l]:
#                print "U [{}] is {}".format(l,m)
#            for n in V[i][l]:
#                print "V [{}] is {}".format(l,n)


    fp2.close()


def yuv2rgb(Y,U,V,dims):  
    U=repeat(U,2,0)  
    U=repeat(U,2,1)  
    V=repeat(V,2,0)  
    V=repeat(V,2,1)  
    r=zeros((dims),float,'C')  
    g=zeros((dims),float,'C')  
    b=zeros((dims),float,'C')  
    rr=zeros((dims),float,'C')  
    gg=zeros((dims),float,'C')  
    bb=zeros((dims),float,'C')  
    rr= Y+1.14*(V-128.0)  
    gg= Y-0.395*(U-128.0)-0.581*(V-128.0)  
    bb= Y+2.032*(U-128.0)          #must be 128.0
  
    rr1=rr.astype(uint8)  
    gg1=gg.astype(uint8)  
    bb1=bb.astype(uint8)  
  
    #print 'rr1:'  
    #print rr1[0:3,0:30]  
      
    return rr1,gg1,bb1 


#===========main============
    #python yuv_lib.py A/420.qcif B/file_out 144 176
if len(sys.argv) != 5:
    print "usage: "
    print "python ****.py (i)A/420.qcif (o)B/file_out w(144) h(176)"
else:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    dims = (int(sys.argv[3]),int(sys.argv[4]))
    numfrm = int(get_frame(input_file,dims))
    data = fuv_read(input_file,dims,numfrm,0)
    i420tonv12(data,dims,numfrm,output_file)
    print "convertion finished"



