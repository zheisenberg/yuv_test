1 what is the yuv file for us to use?
Format	Video Resolution
SQCIF	128 × 96
QCIF	176 × 144
SCIF	256 x 192
SIF(525)	352 x 240
CIF/SIF(625)	352 × 288
4SIF(525)	704 x 480
4CIF/4SIF(625)	704 × 576
16CIF	1408 × 1152
DCIF	528 × 384

----
I will take qcif for simulation
----

2 how do you know if the conversion correct?

----
origin file is org.qcif (i420)
convert it to  dst.qcif (nv12)

convert org.qcif to rgb and print should equle
convert dst.qcif to rgb and print

if we watch org2rgb and dst2rgb, we should find they are identical
to make precise, check the array value, they should be same
----

3 how to avoid the above checking is lying? e.g. the algorithm itself use tricky transformation matrix.

----
convert the org.qcif via ffmpeg or other tools which we believe, and save the converted file as ffmpeg.dst.qcif, compare this to the converted dst.qcif, these two should be identical 

4 what is the algorithm that converts i420 to nv12?

----
i420
                       w
            +--------------------+
            |Y0Y1Y2Y3...         |
            |...                 |   h
            |...                 |
            |                    |
            +--------------------+
            |U0U1      |
            |...       |   h/2
            |...       |
            |          |
            +----------+
            |V0V1      |
            |...       |  h/2
            |...       |
            |          |
            +----------+
                w/2

nv12
                       w
            +--------------------+
            |Y0Y1Y2Y3...         |
            |...                 |   h
            |...                 |
            |                    |
            +--------------------+
            |U0V0U1V1            |
            |...                 |   h/2
            +--------------------+
                       w

convertion is just matrix replacing elements mathematically, no magic.
----

5 what is skipped in this solution?

----
a. there is sometimes header in yuv file, and we need to remove the header, then apply the conversion
b. there is no size checking part for the files, which means we need to specify the size for each file inside the org folder.
   we may add checking function later, one way to do it is check the suffix, but this may not be good enough since it is easy to misname the file with a wrong suffix.
c. for the files inside folder, we may have more later other than 420 only or fuv only, this means later we need regex to get the file we want
d. for folder, they are using absolute path, now we know origin files are in folder A, and dstination file are in folder B, but maybe later we should modify function to creating a folder for 
   dstination, not strict to be B only.
---- 
