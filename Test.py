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
print("Content of AI Answer is: " + response.text)
S1 = response.text

write_file = open("ai_results.txt", "w")
write_file.write(S1)
write_file.close()
#S1 = "Heres how to solve this: 1. **5 + 5 = 10** 2. **√10 ≈ 3.162**  (This is the square root of 10) 3. **10 / 8 = 1.25** (This is 10 divided by 8) Therefore, there\'s ambiguity in the question.  It\'s unclear whether the dividend applies to the sum before or after taking the square root.  The question needs clearer phrasing.  The two possible answers are approximately **3.162** and **1.25**."


file_path = 'transcription_result.txt'

with open(file_path, 'r') as file:
    file_content = file.read()
S2 = file_content
print("Content of answer is: " + S2)
L1 = S1.split()
L2 = S2.split()

FlaggedWordCount = 0
AOF = 0
FlaggedIndexList = []
TempFlaggedIndexList = []

for element in L1:
    inds = 0
    try:
        while L2.index(element, inds) is not None:
            inds += 1
            ind = L1.index(element)
            ind2 = L2.index(element)
            TempFlaggedIndexList = [ind]
            ind += 1
            ind2 += 1
            AOF = 1
            while L1[ind] == L2[ind2] and ind not in FlaggedIndexList:
                TempFlaggedIndexList.append(ind)
                ind += 1
                ind2 += 1
                AOF += 1
            if AOF > 3:
                for i in TempFlaggedIndexList:
                    FlaggedIndexList.append(i)
                FlaggedWordCount += AOF
    except:
        pass
            
print("Flagged " + str(FlaggedWordCount) + " Words:")
for index in FlaggedIndexList:
    print(L1[index], end=" ")
