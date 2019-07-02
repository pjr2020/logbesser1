import os
import json

def labelshorten(labels):
    labels_later = []
    for i in range(len(labels)-1):
        if labels[i] == 5:
            labels_later.append(labels[i+1])
    labels_later.append(5)
    return labels_later

def preprocess(file):
    lines_later = []
    labels = []
    count = 0
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if len(line) > 1:
                if line[-2] == ";":
                    temp = line.lower()
                    if "log" in temp and "(" in temp and ")" in temp:
                        if "warn" in temp:
                            labels += [0]
                        elif "debug" in temp:
                            labels += [1]
                        elif "info" in temp:
                            labels += [2]
                        elif "error" in temp:
                            labels += [3]
                        else:
                            labels += [4]
                    else:
                        labels += [5]
                        lines_later.append(line)
                        count = count + 1
                else:
                    lines_later.append(line)
    labels_later = labelshorten(labels)
    if len(labels_later) != count + 1:
        print("something wrong with java file preprocess: samples and labels do not match")
        return
    with open(os.path.splitext(file)[0]+"_.java", "w") as f:
        f.writelines(lines_later)
    with open(os.path.splitext(file)[0]+"_.json", "w") as f:
        json.dump(labels_later[:-1], f)

# dirs = os.listdir()
# for i in dirs:
#     if os.path.splitext(i)[1] == ".java":
#         preprocess(i)
preprocess("AnytoAny.java")
