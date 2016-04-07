import sys
import os
folder = sys.argv[1]
for root, dirs, files in os.walk(folder):
    for name in files:
        (base, ext) = os.path.splitext(name)
        if ext in ".yuv":
            p = os.path.join(root, name)
            print p
            cmd='python test.py {} B/{}.nv12 144 176'.format(p, base)
            print cmd
            os.system(cmd)
