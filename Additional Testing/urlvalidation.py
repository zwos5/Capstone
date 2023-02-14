import sys
import time
import fromFileTest as fft

print("Hello and welcome to the URLValidator for my capstone project")
time.sleep(2)
print("This script is to run validation tests for URLs for my project")
time.sleep(2)

cont = input("Would you like to run a test? ")
if(cont == "Yes" or cont == "yes" or cont == "Y" or cont == "y"):
    fft.fromFile()
else:
    fft.goodbyeMessage()


print("Made by: Brandon Zwosta")
