import config
from math import log10
from os import rename, path, mkdir
from shutil import move


def merge_lines(line_1, line_2):
    assert line_1[0] == line_2[0]
    # print line_1
    # print line_2
    size = config.FIELDS_SIZE + 1
    i = 1
    j = 1
    line = line_1[0] + "|"
    while i < len(line_1) and j < len(line_2):
        if int(line_1[i]) == int(line_2[j]):
            line += line_1[i] + "|"
            for k in range(size - 1):
                line += str(int(line_1[i+1+k]) + int(line_2[j+1+k])) + "|"
            i += size
            j += size
        elif int(line_1[i]) < int(line_2[j]):
            line += ("|").join(line_1[i:i + size])
            i += size
        else:
            line += ("|").join(line_2[j:j + size])
            j += size
        if line[-1] != "|":
            line += "|"
    line += ("|").join(line_1[i:])
    if line[-1] != "|":
        line += "|"
    line += ("|").join(line_2[j:])
    if line[-1] == "|":
        return line[:-1]
    return line


def process_line(l, num_total_docs):
    line = l[0]
    i = 1
    size = config.FIELDS_SIZE + 1
    num_docs = (len(l) - 1) / size
    idf = log10(num_total_docs / num_docs)
    while i < len(l):
        tf = 0
        line += "|" + l[i]
        for k in range(size - 1):
            if (int(l[i+1+k])):
                tf += int(l[i+1+k])
                line += config.FIELDS[k] + l[i+1+k]
        tf = log10(1 + tf)
        line += "z" + "%.3f" % (tf * idf)
        i += size
    return line

def merge_files(file1_id, file2_id, iteration, out_file = None, num_total_docs = None):
    file1 = config.TEMP_OUT_DIR + str(file1_id)
    file2 = config.TEMP_OUT_DIR + str(file2_id)
    if out_file is None:
        if file1_id == 1:
            out_file = config.TEMP_OUT_DIR + "tmp"
        else:
            out_file = config.TEMP_OUT_DIR + str(file2_id / 2)
        flag = 0
    else:
        flag = 1
    with open(file1, "r") as f_1, open(file2, "r") as f_2, open(out_file, "w") as out:
        l_1 = f_1.readline().rstrip()
        l_2 = f_2.readline().rstrip()
        lines = []
        while l_1 and l_2:
            line_1 = l_1.split("|")
            line_2 = l_2.split("|")
            if line_1[0] == line_2[0]:
                line = merge_lines(line_1, line_2)
                l_1 = f_1.readline().rstrip()
                l_2 = f_2.readline().rstrip()
                # print line
            elif line_1[0] < line_2[0]:
                line = l_1
                l_1 = f_1.readline().rstrip()
            else:
                line = l_2
                l_2 = f_2.readline().rstrip()
            if flag:
                line = process_line(line.split("|"), num_total_docs)
            lines.append(line + "\n")
            if len(lines) == config.MAX_LINES_IN_MEMORY:
                out.writelines(lines)
                lines = []
        while l_1:
            # print l_1
            if flag:
                l_1 = process_line(l_1.split("|"), num_total_docs)
            lines.append(l_1 + "\n")
            l_1 = f_1.readline().rstrip()
            if len(lines) == config.MAX_LINES_IN_MEMORY:
                out.writelines(lines)
                lines = []
        while l_2:
            # print l_2
            if flag:
                l_2 = process_line(l_2.split("|"), num_total_docs)
            lines.append(l_2 + "\n")
            l_2 = f_2.readline().rstrip()
            if len(lines) == config.MAX_LINES_IN_MEMORY:
                out.writelines(lines)
                lines = []
        out.writelines(lines)
        lines = []
    temp_dir = config.TEMP_OUT_DIR + "it" + str(iteration) + "/"
    if not path.exists(temp_dir):
        mkdir(temp_dir)
    move(file1, temp_dir + str(file1_id))
    move(file2, temp_dir + str(file2_id))
    if not flag and file1_id == 1:
        move(out_file, file1)

def merge(length, out_file, num_total_docs):
    iteration = 1
    while length > 1:
        # print length
        if length == 2:
            merge_files(1, 2, iteration, out_file, num_total_docs)
            break
        for i in range(1, length+1, 2):
            if i == length:
                move(config.TEMP_OUT_DIR + str(i),
                     config.TEMP_OUT_DIR + str((i + 1) / 2))
                continue
            merge_files(i, i+1, iteration)
        length = (length + 1) // 2
        iteration += 1
