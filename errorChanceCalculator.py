 #
 #
 #      ErrorChanceCalculator
 #      
 #      Author: Leon Knoke
 #      Date 5.5.22
 #  
 #      Calculates the Chance of each error to occur
 #      according to each given value for 'randomizer'
 #      and therefor allows for comparison and reference
 #      
 #      'randomizer' supports values from 0 to 255
 #
 #      each error has input 1 and 2 as '0'
 #      the folloing errors count upwards in binary using the following inpus (input 3, input4 ...)
 #
 #      if the number of error states is not a power of 2 and <= 8
 #      or an unsued input is defined as '0' on the platform
 #      some error states might not be recognized
 #
 #
 

import random

############## variables editable by user ##############

accuracy = 30000        # number of iterations (>10000 recommeded)

randomizerMin = 0       # minimum Value supported is 0
randomizerMax = 255     # maximum Value supported is 255

numberOfErrorStats = 6  # amount of error states defined on the machine in question

##############            code            ##############

randomizerMin %= 256
randomizerMax %= 256

print("")
print("")
print("Error Chance Calculator")
print("")
print("")
print("randomizer  |\terror1\terror2\terror3\terror4\terror5\terror6\terror7\terror8\t  | total")
print("")

for randomizer in range(randomizerMin, randomizerMax+1):

    error1 = 0
    error2 = 0
    error3 = 0
    error4 = 0
    error5 = 0
    error6 = 0
    error7 = 0
    error8 = 0

    for x in range(accuracy):

        if random.randint(0, 250)< (randomizer+40)%30+10:       
            status = 3                             # chance for an error
            if random.randint(0, 150)< (randomizer+120)%30+34:
                IN = ["0","0","0","0","0","0","0","0"] #ERROR 1
                error1+=1
            elif random.randint(0, 50)< (randomizer+35)%15+3:
                IN = ["0","0","0","1","0","0","0","0"] #ERROR 2
                error2+=1        
            elif random.randint(0, 90)< (randomizer+12)%15+12:
                IN = ["0","0","0","0","1","0","0","0"] #ERROR 3
                error3+=1        
            elif random.randint(0, 90)< (randomizer+69)%15+1:
                IN = ["0","0","0","1","1","0","0","0"] #ERROR 4
                error4+=1        
            elif random.randint(0, 90)< (randomizer+20)%15+15:
                IN = ["0","0","0","0","0","1","0","0"] #ERROR 5
                error5+=1        
            elif random.randint(0, 90)< (randomizer+1)%15+16:
                IN = ["0","0","0","1","0","1","0","0"] #ERROR 6
                error6+=1        
            elif random.randint(0, 60)< (randomizer+90)%15+1:
                IN = ["0","0","0","1","0","1","0","0"] #ERROR 7
                error7+=1        
            else:
                IN = ["0","0","1","1","1","1","0","0"] #ERROR 8
                error8+=1        
    

    if(numberOfErrorStats<=2):
        error1+=error3+error5+error7
        error2+=error4+error6+error8
        error3=0
        error4=0
        error5=0
        error6=0
        error7=0
        error8=0
    elif(numberOfErrorStats<=4):
        error1+=error5
        error2+=error6
        error3+=error7
        error4+=error8
        error5=0
        error6=0
        error7=0
        error8=0
        if(numberOfErrorStats<=3):
            error4=0
    else:
        if(numberOfErrorStats<=5):
            error6=0
        if(numberOfErrorStats<=6):
            error7=0
        if(numberOfErrorStats<=7):
            error8=0


    erGes = error1 + error2 + error3 + error4 + error5 + error6 + error7 + error8
    error1 = round((error1*100/erGes),2)
    error2 = round((error2*100/erGes),2)
    error3 = round((error3*100/erGes),2)
    error4 = round((error4*100/erGes),2)
    error5 = round((error5*100/erGes),2)
    error6 = round((error6*100/erGes),2)
    error7 = round((error7*100/erGes),2)
    error8 = round((error8*100/erGes),2)
    erGes = round((erGes*100/accuracy),2)


    print("  ", randomizer, "\t    |\t", error1, "\t", error2, "\t", error3, "\t", error4, "\t", error5, "\t", error6, "\t", error7, "\t", error8, "\t", " | ", erGes)