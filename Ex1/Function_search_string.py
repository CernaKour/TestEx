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

def phrase_search(object_list: list, search_string: str) -> int:
    h=False
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
                if search_string==del_brackets(i["phrase"]):
                    return i["id"]
                for j in i["slots"]:
                    ex=work_with_string(i["phrase"],j)
                    #print(work_with_string(i["phrase"],j))
                    if search_string==ex:
                        return i["id"]
            if len(i["slots"])>0 and check_on_brackets(i["phrase"]) and check_count_brackets(i["phrase"])==2:
                if search_string==del_brackets(del_brackets(i["phrase"])):
                    return i["id"]
                for j in i["slots"]:
                    sstr=del_brackets(i["phrase"])
                    ex=work_with_string(sstr,j)
                    if search_string==ex:
                        return i["id"]
                for k in i["slots"]:
                    ex=work_with_string(i["phrase"],k)
                    for v in i["slots"]:
                        eex=work_with_string(ex,v)
                        if search_string==eex:
                            return i["id"]
                        
            else:
                ex=i["phrase"]
                if search_string==ex:
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
        {"id": 3, "phrase": "Give me your power", "slots": ["money", "gun"]},
        {"id": 9, "phrase": "I wanna {eat} and {drink}", "slots": ["pizza", "BBQ", "pepsi", "tea"]},
    ]
    #phrase_search(object, 'I wanna pasta')
    #print(phrase_search(object, 'I wanna pasta'))
    print(phrase_search(object, 'I wanna tea and pizza'))
    #assert phrase_search(object, 'I wanna pasta') == 2
    #assert phrase_search(object, 'Give me your power') == 3
    #assert phrase_search(object, 'Hello world!') == 1
    #assert phrase_search(object, 'I wanna nothing') == 0
    #assert phrase_search(object, 'Hello again world!') == 0
    #assert phrase_search(object, 'I need your clothes, your boots & your motorcycle') == 0
