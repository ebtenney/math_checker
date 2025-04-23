import google.generativeai as genai
import os
from collections import Counter
# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# This is the main code for the comparison and getting AI response. You will need an API key and pick a model, which you can obtain at this site for free.
# https://ai.google.dev/gemini-api/docs/api-key

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
def get_shingles(text, n=5):
    words = text.split()
    return Counter([" ".join(words[i:i+n]) for i in range(len(words) - n + 1)])

shingles1 = get_shingles(S1)
shingles2 = get_shingles(S2)


intersection = sum((shingles1 & shingles2).values())
union = sum((shingles1 | shingles2).values())

jaccard_similarity = intersection / union
print("Jaccard Similarity:", jaccard_similarity)
