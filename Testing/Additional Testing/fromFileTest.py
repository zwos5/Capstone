import sys
import time

def fromFile():
    passcount = 0
    failcount = 0

    file1 = open("sampleurls.txt", "r+")
    url_test = list()
    num = file1.readline()
    int(num)

    i = 0

    for i in range(int(num)):
        x = next(file1)
        url_test.append(x)
    i = i + 1
    
    us = '.us'
    gov = '.gov'
    com = '.com'
    net = '.net'
    org = '.org'
    edu = '.edu'
    
    success = next(file1)
    
    j = 0
    for j in range(int(num)):
        if us in url_test[j]:
            print(success)
            passcount = passcount + 1
        elif gov in url_test[j]:
            print(success)
            passcount = passcount + 1
        elif com in url_test[j]:
            print(success)
            passcount = passcount + 1
        elif net in url_test[j]:
            print(success)
            passcount = passcount + 1
        elif org in url_test[j]:
            print(success)
            passcount = passcount + 1
        elif edu in url_test[j]:
            print(success)
            passcount = passcount + 1
        else:
            print("ERROR: " + url_test[j] + " is not a valid url\n")
            failcount = failcount + 1
        j = j + 1
    file1.close()
    
    print("\n============ Test Results ============")

    if(passcount == 1):
        print ("\t", passcount,"test passed ")
    else:
        print ("\t", passcount,"tests passed ")
    
    if(failcount == 1):
        print ("\t", failcount,"test failed ")
    else:
        print ("\t", failcount,"tests failed ")
    
    totaltests = passcount + failcount
    
    resultsfile = open("testresults.txt", "w")
    begin = "Results of the run test: \n"
    resultsfile.write(begin)
    if(passcount == 1):
        resultsfile.write(str(passcount)) 
        resultsfile.write(" test passed")
    else:
        resultsfile.write(str(passcount)) 
        resultsfile.write(" tests passed")
        
    if(failcount == 1):
        resultsfile.write("\n")
        resultsfile.write(str(failcount)) 
        resultsfile.write(" test failed")
    else:
        resultsfile.write("\n")
        resultsfile.write(str(failcount)) 
        resultsfile.write(" tests failed")
    
    resultsfile.write("\n\nPercentage of tests passed: \n")
    resultsfile.write(str(float(passcount/totaltests * 100)))
    resultsfile.write("%")
    
    resultsfile.write("\n\nPercentage of tests failed: \n")
    resultsfile.write(str(float(failcount/totaltests * 100)))
    resultsfile.write("%")
    resultsfile.close()
    
    print("\nResults written to file labeled testresults.txt")

def goodbyeMessage():
    print('Ok goodbye')
