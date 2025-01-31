import google.generativeai as genai
import os
# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

genai.configure(api_key="AIzaSyCocAfdhyrwvn8kJzpfULH7vGcayiC2O80") 
model = genai.GenerativeModel("gemini-1.5-flash")

file_path = 'problem.txt'
with open(file_path, 'r') as file:
    file_content = file.read()
response = model.generate_content(file_content)
print(response.text)
S1 = response.text

file_path = 'answer.txt'

with open(file_path, 'r') as file:
    file_content = file.read()
S2 = file_content

L1 = S1.split()
L2 = S2.split()

FlaggedWordCount = 0
AOF = 0
FlaggedIndexList = []
TempFlaggedIndexList = []


for element in L2:
	inds = 0
	try:
		while L1.index(element, inds) is not None:
			ind = L1.index(element)
			inds = ind + 1
			ind2 = L2.index(element)
			AOF = 1
			TempFlaggedIndexList = []
			TempFlaggedIndexList.append(ind)
			ind += 1
			ind2 += 1
			while (L1[ind] == L2[ind2]):
				TempFlaggedIndexList.append(ind)
				ind += 1
				ind2 += 1
				AOF += 1
			if AOF >= 3:
			    for i in TempFlaggedIndexList:
			    	FlaggedIndexList.append(i)
			    FlaggedWordCount += AOF
	except:
		inds = 0
            
print(FlaggedWordCount)
for index in FlaggedIndexList:
    print(L1[index], end=" ")
