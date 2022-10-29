import os

data_dirs = [ 
    "basement", 
    "childsroom", 
    "diningroom", 
    "frontporch",
    "kitchen",
    "livingroom",
    "studio"
    ] 

path = "input-videos/"

vidfiles = []
counts = {}
for dirpath, subdirs, files in os.walk(path):
    for x in files:
        if x.endswith(".mp4"):
            lastsubfolder = dirpath.split("/")[-1]
            if lastsubfolder in data_dirs:
                if lastsubfolder in counts:
                    counts[lastsubfolder]+=1
                else:
                    counts[lastsubfolder]=1
                vidfiles.append(os.path.join(dirpath, x))

print(vidfiles[:10])
print(vidfiles[-10:])
print(counts, sum(counts.values()))