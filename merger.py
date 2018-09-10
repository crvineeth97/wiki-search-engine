import config
from os import rename

def mergeFiles(file1_id, file2_id):
    file1 = config.TEMP_OUT_DIR + str(file1_id)
    file2 = config.TEMP_OUT_DIR + str(file2_id)
    if file1_id == 1:
        out_file = config.TEMP_OUT_DIR + "tmp"
    else:
        out_file = config.TEMP_OUT_DIR + str(file2_id / 2)
    with open(file1, "r") as f1, open(file2, "r") as f2, open(out_file, "w") as w:
        l1 = f1.readline()
        l2 = f2.readline()
        while l1 and l2:
            line1 = l1.split("|")
            line2 = l2.split("|")
            


    if file1_id == 1:
        rename(out_file, file1)
