d = 10



def search(pattern, text, q):
    m = len(pattern)
    n = len(text)
    p = 0
    t = 0
    h = 1
    i = 0
    j = 0
    count = 0

    for i in range(m-1):
        h = (h*d) % q

    # Calculate hash value for pattern and text
    for i in range(m):
        p = (d*p + ord(pattern[i])) % q
        t = (d*t + ord(text[i])) % q

    # Find the match
    for i in range(n-m+1):
        if p == t:
            for j in range(m):
                if text[i+j] != pattern[j]:
                    break

            j += 1
            if j == m:
                count +=1
                # print("Pattern is found at position: " + str(i+1)+". match: "+text[i-1])

        if i < n-m:
            t = (d*(t-ord(text[i])*h) + ord(text[i+m])) % q

            if t < 0:
                t = t+q
    
    return count


text = open("ai_results.txt", "r").read()
pattern = open("transcription_result.txt","r").read()
word_list = pattern.split(" ")

# q = 13
result = 0
# print (word_list)
count = 0

for i in range(1,len(word_list)):
    for j in range(len(word_list)-i):
        word = ""
        for k in range(i,j):
            word+=word_list[k]
        word.replace(" ","")
        if word == "":
            continue
        result += search(word, text, 13)
        count += 1
    
print(f"found {result} matches out of {count} checks")