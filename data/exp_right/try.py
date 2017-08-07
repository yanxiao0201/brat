import os, glob

print glob.glob('*after*')

for i in glob.glob('*after*'):
    words = i.split('_')

    newname = words[0] + '_' + words[-1]

    os.rename(i, newname)
