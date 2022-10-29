import os, sys
import shutil

indir = "output/"
outdir = "output_renumbered/"
for subdir, dirs, files in os.walk(indir):
    for file in files:
        if file.split(".")[1] == "jpg":
            # print(file, subdir)
            # sys.stdout.flush()
            splits = subdir.split("_")
            just_time = splits[-3]+"_"+splits[-2]
            frame_num = file.split("_")[-1]
            # print(os.path.join(subdir, file), end="")
            room_name = subdir.split("/")[1]
            new_name = room_name+"_"+just_time+"_"+frame_num
            outpath = os.path.join(outdir, new_name)
            inpath = os.path.join(subdir, file)
            print(inpath, " -> ", outpath)
            shutil.copy(inpath, outpath)