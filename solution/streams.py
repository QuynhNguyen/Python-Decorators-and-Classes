from misc import *
import crypt

#easy str splitting
def words_in_line(l):
    return str.split(l)

def streamify(f):
    #inner function which will be returned by streamify
    def helper(l):
        #this function will take in an object which may be iterate over
        for x in l:
            for each in f(x):
                #return an iterable object
                yield each
    return helper       

### uncomment the following when you have everything working!
words_in_file = compose(streamify(words_in_line),open)

### put your transformation code here

def transform_reverse(str):
    if(len(str) >= 6 and len(str) <= 8):
        reverse_list = [] #Empty List
        reverse_string = "" #Empty string to store reverse string
    
        x = len(str)-1 #total string length - 1
    
        #making a new string by concatenating string[n-1] + string[n-2] + ...+ String[0]
        while (x >= 0):
            reverse_string = reverse_string + str[x]
            x = x -1
    
        #Add it to the list  
        reverse_list.append(str)
        reverse_list.append(reverse_string)
        
        return reverse_list
    else:
        return ""



def transform_capitalize(str):
    
    x = [] 

    #Use recursive with the help of helper function
    #Here is how it work:
    #let say our input string is abcd
    #we will get Abcd then recurse on Abcd which is ABcd then recursive on that
    #if we keep doing that then at the end we will have all the combination
     
    def helperFun(n,list,str):
            if(str not in list):
                list.append(str)
            #list.append(str) #add it to the list
            for i in range(n,len(str)):
                temp = str[0:i] + str[i].upper() + str[i+1:]
                helperFun(i+1, list, temp) #recurse begin on the next char of the string
            return list
    if(len(str) >= 6 and len(str) <= 8):
        return helperFun(0,x,str) #call the recursive function 
    else:
        return ""   
    
    

def transform_digits(str):
    #add the map dictionary
    l33tDict = {'o':['0'], 'z':['2'], 'a':['4'], 'b':['6','8'], 'i':['1'], 'l':['1'], 'e':['3'], 's':['5'], 't':['7'], 'g':['9'], 'q':['9']}
    myList = [] #initiate an empty list

    #This function is almost exactly the same as the transform_capitalize
    #Main different is that you have to check if there is something inside
    #the dictionary list before transforimg it. If there is none, then
    #dont mess around with it.
    def helperFun(n,list,str):
            if(str not in list):
                list.append(str)
            #list.append(str)
            for i in range(n,len(str)):
                if(l33tDict.has_key(str[i].lower())):
                    numList = l33tDict[str[i].lower()]
                    for j in range(0, len(numList)):
                        temp = str[0:i] + numList[j] + str[i+1:]
                        helperFun(i+1, list, temp)
            return list
    if(len(str) >= 6 and len(str) <= 8):
        return helperFun(0,myList,str)
    else:
        return ""



#compose(streamify(transform_reverse),compose(streamify(words_in_line),open))
#nested compose function to get all the possible combination
transformed_words_in_file = compose(streamify(transform_capitalize),compose(streamify(transform_digits),compose(streamify(transform_reverse),compose(streamify(words_in_line),open))))
#transformed_words_in_file = compose(streamify(transform_capitalize),compose(streamify(words_in_line),open))                               

def crack_pass_file(fn_pass,fn_words,fn_out):
    """Crack as many passwords in file fn_pass as possible using words
       in transformed_words_in_file(fn_words)"""
    ts=[l.split(":") for l in open(fn_pass,"r")]
    pw=[(t[0],t[1]) for t in ts]
    fout=open(fn_out,"w")
    for w in transformed_words_in_file(fn_words):
        for a,p in pw:
            if crypt.crypt(w,p)==p:
                fout.write("%s=%s\n" % (a,w))
                fout.flush()
    fout.close()
