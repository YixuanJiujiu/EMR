#Bayes Network
def BayesNetwork(text):
    # A simple example of the conversation
    # This information will be pass by the speech recognize API( text[i] = marker + r.recognize_google(audio[i]) )
    # Note: recognize result from Google Speech API does not include any punctuation
    # A sample keyword database
    # The actual database should be generated by SQL or a Spider
    keywordindex = ["Name", "Information", "History", "Billing", "Symptoms", "Allergy", "Family", "Organ","Be"]
    keywordcategory = []
    keywordcategory.append("")
    #Name
    keywordcategory[0] = {"am","I'm"}
    keywordcategory.append("")
    #Information
    keywordcategory[1] = {"centimeter","centimeters","meter","meters","inch","inchs","worker", "student" , "teacher", "professor"}
    keywordcategory.append("")
    #Time
    keywordcategory[2] = {"days","day","weeks","week","year","years","month","months","recent","recently","current","time"}
    keywordcategory.append("")
    #Billing
    keywordcategory[3] = {"worker", "student" , "teacher", "professor"}
    keywordcategory.append("")
    #Symptoms
    keywordcategory[4] = {"cough", "coughed", "coughing", "fever", "ache", "itch","headache"}
    keywordcategory.append("")
    #Allergy
    keywordcategory[5] = {"penicillins" , "aspirins"}
    keywordcategory.append("")
    #Family
    keywordcategory[6] = {"father" , "mother", "dad", "mom", "grandpa", "grandma", "son", "daugher", "sister", "brother", "cousin", "wife", "husband"}
    keywordcategory.append("")
    #Organ
    keywordcategory[7] = {"head","eye","eyes","nose","ear","ears","mouth","leg","legs","heart","arm","arms","lung","lungs"}
    keywordcategory.append("")
    #Be
    keywordcategory[8] = {"is","am","are","was","were","be"}

    # Splitting the text, and make the text not sensitive to the upper/lower cases
    textsplit = []
    print(text)
    textsplit = text.split()
        #for i in range (0, len(text)):
        #text[i] = text[i].lower()
        #textsplit.append(text[i].split())
    #print (textsplit[i])
    
    # Analyzing the text (Keyword Comparing)
    record = []
    for k in range (0, len(keywordcategory)):
        record.append([])


    cateLookUp = {"Name":0, "Information": 1, "Time":2 , "Billing": 3, \
    			"Symptoms": 4, "Allergy": 5, "Family":6, "Organ":7,"Be":8}
    tag = []
    for o in range(0,len(textsplit)):
        tag.append(0)

    for j in range (0, len(textsplit)):
        for k in range (0, len(keywordcategory)):
            if textsplit[j] in keywordcategory[k] :
                        tag[j] = k
                        record[k].append(textsplit[j])
                        if k == 4 :
                            print("symptom detected")
                            #record[k].append(textsplit[j])
                            if k == 0 :
                                print("name detected")
                                #record[k].append(textsplit[j+1])
                        if k == 1 or k == 2:
                            print("time detect")
                            #record[k].append(textsplit[j-1])

	#Bayes Network

	# Symptom layer, detect symptoms
    if (len(record[cateLookUp['Symptoms']]) > 0):
		# Family Layer, detect family members
		if (len(record[cateLookUp['Family']]) > 0):
			# Report Family history
			print('Report Family history')
			print(record[cateLookUp['Family']][0] + " : " + record[cateLookUp['Symptoms']][0])
		# Time Layer, detect Time information
		elif (len(record[cateLookUp['Time']]) > 0):
			# Long period
			if ("year" in record[cateLookUp['Time']] \
				or "years" in record[cateLookUp['Time']]):
				# Report Problem list
				print('Report Problem list')
				print(record[cateLookUp['Symptoms']])

			else: 
				# Report History of present illness
				print('Report HPI')
		                print(record[cateLookUp['Symptoms']][0] + " for " + record[cateLookUp['Time']][0])
		else: 
			# Report Problem list
			print('Report Problem list')
			print(record[cateLookUp['Symptoms']])


	# No symptom found, detect organ
    elif (len(record[cateLookUp['Organ']]) > 0): 
		# Report phycial Exam
		print('Report phycial Exam')
		print(text)

	# No organ found, check for special set
    else: 
	print('Enter special sets')
                    #End the Conversation
        if (("all" in textsplit) and ("bye" in textsplit)):
                print("Conversation End")
                exit(0)

        if (("questions" in textsplit) and ("yes" in textsplit) and ("no" in textsplit)):
                negatives_flag = 1

        #Output the extracting results
    for i in range (0, len(keywordcategory)):
        print (keywordindex[i])
        print (record[i])
    return 1

BayesNetwork("I have fever and headache for days")
