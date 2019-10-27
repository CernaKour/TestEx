def check_count_brackets(check_string: str) -> int:
    a=check_string.find("{")
    s=check_string[a+1:]
    b=s.find("{")
    if b!=-1:
        return 2
    elif a!=-1:
        return 1
    else:
        return 0
    
def check_on_brackets(check_string: str) -> bool:
    s=[]
    for i in check_string:
        if i=='{':
            s.append("{")
        elif len(s)!=0 and i=='}':
            s.remove("{")
        elif len(s)==0 and i=='}':
            return False
    if len(s)!=0:
        return False
    else:
        return True

def work_with_string(sphrase:str,schange:str)->str:
    a=sphrase.find("{")
    b=sphrase.find("}")
    s=sphrase[a:b+1]
    return sphrase.replace(s,schange)

def del_brackets(sphrase:str)->str:
    a=sphrase.find("{")
    b=sphrase.find("}")
    s=sphrase.replace("{","",1)
    sphrase=s.replace("}","",1)
    return sphrase


def levenshtein_distance(s, t,ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    #print(rows)
    cols = len(t)+1
    #print(cols)
    distance = [[0 for n in range(cols)] for m in range(rows)]
    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            #print(distance[i][0])
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return distance[row][col]





def phrase_search(object_list: list, search_string: str) -> int:
    h=False
    q=1  #count mistake
    for i in object_list:
        if len(i)==0:
            h=False
        elif i["id"] > 0 and 0<=len(i["phrase"]) and len(i["phrase"])<=120 and 0<=len(i["slots"]) and len(i["slots"])<=50:
            h=True
        else:
            object_list.remove(i)
    if h:
        for i in object_list:
            if len(i["slots"])>0 and check_on_brackets(i["phrase"]) and check_count_brackets(i["phrase"])==1:
                if levenshtein_distance(search_string,del_brackets(i["phrase"]))<q+1:
                    return i["id"]
                for j in i["slots"]:
                    ex=work_with_string(i["phrase"],j) #first section
                    #print(work_with_string(i["phrase"],j))
                    if levenshtein_distance(search_string,ex)<q+1:
                        return i["id"]
            if len(i["slots"])>0 and check_on_brackets(i["phrase"]) and check_count_brackets(i["phrase"])==2:
                if levenshtein_distance(search_string,del_brackets(del_brackets(i["phrase"])))<q+1: #null section
                    return i["id"]
                for j in i["slots"]:
                    sstr=del_brackets(i["phrase"]) 
                    ex=work_with_string(sstr,j) # first section
                    if levenshtein_distance(search_string,ex)<q+1:
                        return i["id"]
                for k in i["slots"]:
                    ex=work_with_string(i["phrase"],k) 
                    for v in i["slots"]:
                        eex=work_with_string(ex,v) # second section
                        if levenshtein_distance(search_string,eex)<q+1:
                            return i["id"]
                        
            else:
                ex=i["phrase"]
                #print(search_string)
                if levenshtein_distance(search_string,ex)<q+1:
                    return i["id"]
    return 0





if __name__ == "__main__":
    """ 
    len(object) != 0
    object["id"] > 0
    0 <= len(object["phrase"]) <= 120
    0 <= len(object["slots"]) <= 50
    """
    object = [
        {"id": 1, "phrase": "Hello world!", "slots": []},
        {"id": 2, "phrase": "I wanna {pizza}", "slots": ["pizza", "BBQ", "pasta"]},
        {"id": 5, "phrase": "I wanna {eat}", "slots": ["pizza", "BBQ", "pasta"]},
        {"id": 3, "phrase": "Give me your power", "slots": ["money", "gun"]},
        {"id": 9, "phrase": "I wanna {eat} and {drink}", "slots": ["pizza", "BBQ", "pepsi", "tea"]},
    ]
    #phrase_search(object, 'I wanna pasta')
    #print(phrase_search(object, 'I wanna pasta'))
    #print(levenshtein_distance('I wanna pasta','I wanna pasta'))
    assert phrase_search(object, 'I wanna eat') == 5
    assert phrase_search(object, 'I wanna tea and pizza') == 9
    assert phrase_search(object, 'I wanna pasta') == 2
    assert phrase_search(object, 'i wanna pasta') == 2
    assert phrase_search(object, 'Give me your power') == 3
    assert phrase_search(object, 'Hello world!') == 1
    assert phrase_search(object, 'I wanna nothing') == 0
    assert phrase_search(object, 'Hello again world!') == 0
    assert phrase_search(object, 'I need your clothes, your boots & your motorcycle') == 0
