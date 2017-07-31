import os, glob

print glob.glob('*before*')

for i in glob.glob('*before*'):
    words = i.split('_')

    newname = words[0] + '_' + words[-1]

    os.rename(i, newname)
