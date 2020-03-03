import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


file1 = os.path.join(os.getcwd(),'hmm-training-data', 'it_isdt_dev_tagged.txt')
file2 = os.path.join(os.getcwd(),'hmmoutput.txt')
trueN = 0
Num = 0



if __name__ == "__main__":
    tag = open(file1,'r')
    output = open(file2,'r')
    arr = tag.readlines()
    arr2 = output.readlines()
    minT = min(len(arr),len(arr2))
    print minT
    for i in range(minT):
        # print (len(arr[i]),len(arr2[i]))
        tmpA = re.split(' ',arr[i])
        tmpB = re.split(' ',arr2[i])

        # print arr[i]
        minN = min(len(tmpA),len(tmpB))
        for j in range(minN):
            # print  tmpA[j],tmpB[j]
            Num += 1
            if (len(re.split('/',tmpA[j])) > 1) and (len(re.split('/',tmpB[j])) > 1):
                if (re.split('/',tmpA[j])[1].strip() == re.split('/',tmpB[j])[1].strip()):
                    trueN += 1
                else:
                    print j, minN,re.split('/',tmpA[j])[0].strip() , re.split('/',tmpA[j])[1].strip() ,re.split('/',tmpB[j])[1].strip()

        # for j in range(min(len(arr[i]),len(arr2[i]))):

    print 1.0*trueN/Num