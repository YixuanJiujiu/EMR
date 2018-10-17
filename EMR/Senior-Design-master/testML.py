
import speech_recognition as sr
import threading
from threading import Thread, current_thread
import time
from multiprocessing import Process, Queue, Manager 
import datetime
import sklearn.datasets
from sklearn.datasets import load_files
import sklearn.metrics
import sklearn.svm
import sklearn.naive_bayes
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import sklearn.neighbors
from sklearn import svm
import sys, os, glob
from pprint import pprint

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer




def HardClassify(text):
        # A simple example of the conversation
        # This information will be pass by the speech recognize API( text[i] = marker + r.recognize_google(audio[i]) )
        # Note: recognize result from Google Speech API does not include any punctuation
        """
            text = []
            text.append("")
            text[0] = "[D] Hello Mr Potter could you please talk something about yourself"
            text.append("")
            text[1] = "[P] Hello Dr Ingham I am Harry Potter a student 21 years old 170 centimeters height 65 kilograms weight Currently catched a cold"
            text.append("")
            text[2] = "[D] What are the symptoms that trouble you Specifically"
            text.append("")
            text[3] = "[P] I have been coughing for half a week and have been running a fever"
            text.append("")
            text[4] = "[D] I see and do you allergy to any kind of medicine"
            text.append("")
            text[5] = "[P] Might be Penicillins my former doctor told me don't use that"
            
            """
        # A sample keyword database
        # The actual database should be generated by SQL or a Spider
        keywordindex = ["Me", "You", "Information", "Time", "Billing", "Symptoms", "Allergy", "Family", "Organ","Be","Medicine","Instructions","Terms","Disease","Test"]
        keywordcategory = []
        keywordcategory.append("")
        #Me
        keywordcategory[0] = {"am","I'm"}
        keywordcategory.append("")
        #You
        keywordcategory[1] = {"You","you're","your"}
        keywordcategory.append("")
        #Information
        keywordcategory[2] = {"centimeter","centimeters","meter","meters","inch","inchs","worker", "student" , "teacher", "professor"}
        keywordcategory.append("")
        #Time
        keywordcategory[3] = {"days","day","weeks","week","year","years","month","months","recent","recently","current","time"}
        keywordcategory.append("")
        #Billing
        keywordcategory[4] = {"worker", "student" , "teacher", "professor"}
        keywordcategory.append("")
        #Symptoms
        keywordcategory[5] = {"cough", "coughed", "coughing", "fever", "ache", "itch","headache","temperature","worn"}
        keywordcategory.append("")
        #Allergy
        keywordcategory[6] = {"penicillins" , "aspirins","drug allergy"}
        keywordcategory.append("")
        #Family
        keywordcategory[7] = {"father" , "mother", "dad", "mom", "grandpa", "grandma", "son", "daugher", "sister", "brother", "cousin", "wife", "husband"}
        keywordcategory.append("")
        #Organ
        keywordcategory[8] = {"head","eye","eyes","nose","ear","ears","mouth","leg","legs","heart","arm","arms","lung","lungs","wrist","facial","face","arches","hand","nose","oral","vaginal"}
        keywordcategory.append("")
        #Be
        keywordcategory[9] = {"is","am","are","was","were","be"}
        keywordcategory.append("")

        #Medicine
        keywordcategory[10] = {"antibiotic","Ora","film","cardolor","calomist","catapres","jalyn","Jetrea","fish oil","citamin B","Tarka","Tcis","Temodar","Yervoy","YAZ","saizen","salacyn","vitamin","uceris","jetrea","wellbutrin"}
        keywordcategory.append("")

        #Instructions
        keywordcategory[11] = {"rest","work","smoking","medication","water","exercises","fruit","vegetables","surgery","hospital","food"," water","sleep","meat"}
        keywordcategory.append("")

        #Terms
        keywordcategory[12] = {"swollen","yellow","wisdom","fracture","palsy","fallen","broken","fluid","hip","obesity"}
        keywordcategory.append("")
        #Disease
        keywordcategory[13] = {"obesity","cancer","candidiasis","varicella","variola","acne","baldness","itch","Benign","migratory","glossitis","blackheads","infection","overactive" ,"thyroid","fever","retinopathy","diabetic"}
        keywordcategory.append("")
        #Test
        keywordcategory[14] = {"test","hida","scan","hiv","testing","hpv","a1c","bone","ct","cancer","screening","density","blood","pressure","bun","nonstress","x-ray","xray","genetic","ferritin","tile","table"}
        keywordcategory.append("")
        # Splitting the text, and make the text not sensitive to the upper/lower cases
        textsplit = []
        textsplit = text.split()
            #for i in range (0, len(text)):
            #text[i] = text[i].lower()
            #textsplit.append(text[i].split())
        #print (textsplit[i])
        
        # Analyzing the text (Keyword Comparing)
        record = []
        for k in range (0, len(keywordcategory)):
            record.append([])


        cateLookUp = {"Me":0,"You": 1, "Information": 2, "Time": 3, "Billing": 4, \
            "Symptoms": 5, "Allergy": 6, "Family": 7, "Organ": 8,"Be": 9,"Medicine": 10, \
            "Instructions": 11,"Terms": 12,"Disease":13,"Test":14}
        tag = []
        Detected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for o in range(0,len(textsplit)):
            tag.append(0)

        for j in range (0, len(textsplit)):
            for k in range (0, len(keywordcategory)):
                if textsplit[j] in keywordcategory[k] :
                            Detected[k] = 1
                            tag[j] = k
                            record[k].append(textsplit[j])
                            if k == 5 :
                                print("symptom detected")
                                #record[k].append(textsplit[j])
                                if k == 0 :
                                    print("name detected")
                                    #record[k].append(textsplit[j+1])
                            if k == 1 or k == 2:
                                print("time detect")
                                #record[k].append(textsplit[j-1])

        #Decision Tree Network
        VoteD = "Special_Sets"
        # Symptom layer, detect symptoms
        if (len(record[cateLookUp['Disease']]) > 0):
            # Family Layer, detect family members
            if (len(record[cateLookUp['Family']]) > 0):
                # Report Family history
                VoteD = 'Family_History'
                print('Report Family history')
                #print(record[cateLookUp['Family']][0] + " : " + record[cateLookUp['Symptoms']][0])
            if (len(record[cateLookUp['You']]) > 0):
                # Report Assessment
                VoteD = 'Assessment'
                print('Report Assessment')
            # Time Layer, detect Time information
            elif (len(record[cateLookUp['Time']]) > 0):
                # Long period
                if ("year" in record[cateLookUp['Time']] \
                    or "years" in record[cateLookUp['Time']]):
                    # Report Problem list
                    VoteD = 'Medical_History'
                    print('Report Medical History')
                    #print(record[cateLookUp['Symptoms']])
                else: 
                    # Report History of present illness
                    VoteD = 'HPI'
                    print('Report HPI')
                    #print(record[cateLookUp['Symptoms']][0] + " for " + record[cateLookUp['Time']][0])
            else: 
                # Report Medical History
                VoteD = 'Medical_History'
                print('Report Medical History')
                #print(record[cateLookUp['Symptoms']])

        elif (len(record[cateLookUp['Symptoms']]) > 0):
            if (len(record[cateLookUp['Time']]) > 0):
                VoteD = 'HPI'
                print('Report HPI')
        # No symptom found, detect organ
        elif (len(record[cateLookUp['Organ']]) > 0):
            if (len(record[cateLookUp['Terms']]) > 0):
            # Report phycial Exam
                VoteD = 'Physical_Exam'
                print('Report physical Exam')
                #print(text)
        # check allergy
        elif (len(record[cateLookUp['Allergy']]) > 0):
            VoteD = 'Allergy'
            print('Report allergy')

        elif (len(record[cateLookUp['Me']]) > 0):
            if (len(record[cateLookUp['Medicine']]) > 0):
                VoteD = 'Medications'
                print('Report Medications')

        elif (len(record[cateLookUp['You']]) > 0):
            if (len(record[cateLookUp['Instructions']]) > 0):
                VoteD = 'Instructions'
                print('Report Patient Instructions')
            elif (len(record[cateLookUp['Test']]) > 0):
                VoteD = 'Plan'
                print('Report Plan')
        else:
            VoteD = 'Special_Sets'
            print('Enter special sets')
                        #End the Conversation
            if (("all" in textsplit) and ("bye" in textsplit)):
                    print("Conversation End")
                    exit(0)

            if (("questions" in textsplit) and ("yes" in textsplit) and ("no" in textsplit)):
                    negatives_flag = 1








        #Naive Fixed Bayes


        #Currently four kinds of outputs enabled.


        cateLookUp = {"Me":0,"You": 1, "Information": 2, "Time": 3, "Billing": 4,"Symptoms": 5, "Allergy": 6, "Family": 7, "Organ": 8,"Be": 9,"Medicine": 10,"Instructions":11,"Terms": 12,"Disease":13,"Test":14}
        ResultLookUp = ["Allergy","Assessment","Family_History","HPI",\
                        "Medcial_History","Medications","Instructions",\
                        "Physical_Exam","Plan","Review"]
        ResultProbB = [1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
#                        0   1   2   3   4   5   6   7   8   9   10  11  12  13  14
        BayesTable = [ [0.5,0.1,0.1,0.1,0.1,0.2,0.9,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.3], \
                       [0.1,0.5,0.1,0.1,0.1,0.5,0.3,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.4], \
                       [0.3,0.1,0.1,0.1,0.1,0.5,0.1,0.8,0.1,0.1,0.1,0.1,0.1,0.8,0.2], \
                       [0.7,0.1,0.1,0.6,0.1,0.9,0.1,0.1,0.5,0.1,0.1,0.1,0.1,0.8,0.3], \
                       [0.7,0.1,0.1,0.8,0.1,0.6,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.9,0.3], \
                       [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1], \
                       [0.4,0.7,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.7,0.1,0.1,0.4], \
                       [0.5,0.6,0.1,0.1,0.1,0.6,0.1,0.1,0.7,0.1,0.1,0.1,0.8,0.5,0.1], \
                       [0.4,0.6,0.1,0.1,0.1,0.4,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.5,0.8], \
                       [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1], \
                      ]




        for i in range(0,len(ResultProbB)) :
            for j in range(0,len(BayesTable[i])) :
                if Detected[j] == 1:
                    ResultProbB[i] = ResultProbB[i] * BayesTable[i][j]
                else:
                    ResultProbB[i] = ResultProbB[i] * 0.5
        ##print("The result of Bayes Table:")
        largest = 0
        largestindex = 0
        for i in range(0,len(ResultProbB)) :
         ##   print(ResultProbB[i])
            if ResultProbB[i] > largest:
                largest = ResultProbB[i]
                largestindex = i
        print(ResultLookUp[largestindex])

        VoteB = ResultLookUp[largestindex]
        print("vote result")
        print(VoteB,VoteD)
'''
        if VoteB == VoteD :
            print("Quite sure about the classify result, generating training data")
            currenttime = datetime.datetime.now()
            currenttime = ''.join(["Date:",str(currenttime)])
            filename = ''.join([currenttime,".txt"])
            fullfilename = ''.join([VoteB,"/",filename])
            trainingfile = open(fullfilename,"w")
            trainingfile.write(text)
            trainingfile.close
'''


            #Output the extracting results
        #for i in range (0, len(keywordcategory)):
            #print (keywordindex[i])
            #print (record[i])
        return VoteB,VoteD





def MLClassify(text):

    '''
    test_path = './testing'
    test_files = sklearn.datasets.load_files(test_path, encoding = 'latin1', load_content=True)
    #
    # print(test_files)
    print("test_files")
    print(test_files.data)
    X_test_counts = count_vect.transform(test_files.data)
    print("X_test_counts")
    print(X_test_counts.toarray())
    X_test_tfidf = tfidf_transformer.transform(X_test_counts)
    print("X_test_tfidf")
    print(X_test_tfidf.toarray())
    # print(X_test_counts.shape)
    predicted = svm.predict_proba(X_test_counts)
    #
    print("svm.predict")
    print(svm.predict(X_test_counts))
    print("predicted")
    print(predicted)
    '''

    #count_vect = CountVectorizer()
    #print("train",files)
    X_test_countst = count_vect.transform([text])

    X_test_tfidft = tfidf_transformer.transform(X_test_countst)
    predict_result = svmi.predict_proba(X_test_tfidft)
    print("test = " , svmi.predict_proba(X_test_tfidft))
    print(predict_result.shape)
    #print(predict_result[0][1])
    #print(predict_result.shape[1])
    print(svmi.predict(X_test_countst))
    #print(X_test_countst.toarray())
    MLcategory = ["Allergies","Assessment","Family_History","HPI","Medical_History","Medications","Patient_Instructions","Physical_Exam","Plan","Review_of_Systems"]
    print(MLcategory[svmi.predict(X_test_countst)[0]])
    return MLcategory[svmi.predict(X_test_countst)[0]]







path = './dataset'
files = sklearn.datasets.load_files(path, encoding = 'latin1', decode_error = 'replace', load_content=True, random_state=3)
# print(files)
count_vect = CountVectorizer()

X_train_counts = count_vect.fit_transform(files.data)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# print(X_train_tfidf)
# print("Target")
# print(files)
# print()
# print((X_train_counts))
svmi = svm.SVC(kernel = 'linear', probability=True)
X = X_train_tfidf
# pprint(files.values())
Y = files["target"]
print("Shapes")
print(X.shape)
print(Y.shape)
h = svmi.fit(X, Y)
print(h)


MLClassify("Patient: I am coughing for years")
MLClassify("Doctor: Can you take some Aspirin")
MLClassify("Patient: My dad has headache")
MLClassify("Doctor: Your eyes looks yellow")


HardClassify("Patient: i am coughing for years")
HardClassify("Doctor: you take some aspirin")
HardClassify("Patient: my dad has headache")
HardClassify("Doctor: your eyes looks yellow")