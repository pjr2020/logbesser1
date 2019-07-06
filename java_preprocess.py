import os
import json
def lineProcessing(file):
    code = []
    flag = 0
    f = open(file, 'r+')
    for line in f:
        place=line.find('//')
        if(place >= 0):
            line=line[0:place]
        line=line.strip()
        if(line=='' or line[0]=='*' or line[0:2]==r"/*"):
            continue
        if flag==0:
            code.append(line)
        else:
            code[len(code)-1]=code[len(code)-1]+' '+line
        if(line[len(line)-1] in ('{',';','}')):
            flag=0
        else:
            flag=1
    '''for i in code:
        print(i)'''
    f.close()
    return code

def labelshorten(labels):
    labels_later = []
    for i in range(len(labels)-1):
        if labels[i] == 5:
            labels_later.append(labels[i+1])
    if(labels[len(labels)-1]==5):
        labels_later.append(5)
    return labels_later

def preprocess(file):
    code= lineProcessing(file)
    lines_later = []
    labels = []
    for line in code:
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
            lines_later.append(line+'\n')
    labels_later = labelshorten(labels)
    print(len(lines_later),len(labels_later))
    with open(os.path.splitext(file)[0]+"_.java", "w") as f:
        f.writelines(lines_later)
    with open(os.path.splitext(file)[0]+"_.json", "w") as f:
        json.dump(labels_later[:-1], f)

# dirs = os.listdir()
# for i in dirs:
#     if os.path.splitext(i)[1] == ".java":
#         preprocess(i)
if __name__=='__main__':
    preprocess("EnvironmentInformation.java")
