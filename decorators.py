from misc import Failure


class profiled(object):
    def __init__(self,f):
        self.__count=0
        self.__f=f
        self.__name__=f.__name__
    def __call__(self,*args,**dargs):
        self.__count+=1
        return self.__f(*args,**dargs)
    def count(self):
        return self.__count
    def reset(self):
        self.__count=0

class traced(object):
    __count = 0
    def __init__(self,f):
        # replace this and fill in the rest of the class
        self.__name__= f.__name__ #assign class name to be function name
        self.__f = f #assign local variable for function
        self.__printString = ""

        
    #function to retrun total number of count
    def count(self):
        return self.__count #return how many time you recursed
    
    #reset count
    def reset(self):
        self.__count = 0 #reset number of count
        
    #check when a function is called
    def __call__(self,*args,**dargs):
        #find the legnth of the args
        length_args = len(args)
        #find the length of dict
        length_dict = len(dargs)
        #local variable to keep track of the loop
        i = 0
        #print out the pipe depend on how many function called so far
        for x in range(self.count()):
            print "| ",
        
        #various character append to string
        printString = ",- " + self.__name__ + "("
        
        #if the length of args is bigger than 0 
        #then find the list of all the argument
        if(length_args > 0):
            for x in args:
                printString += repr(x)
                if(i != length_args-1):
                    printString += ', '
                i += 1
        else:
            #otherwise, we know we have to find all the dictionary and its name
            #once we found it, store all of them for print out later
            printString += ''
            for key in dargs:
                printString += key + "=" + repr(dargs[key])
                #to check and not printing out the last coma
                if(i != length_dict-1):
                    printString += ', '
                i += 1
        #closing paren.
        printString += ")"
        #print everything out
        print printString
        
        #increase the trace count
        traced.__count = traced.__count + 1
        
        
        try:
            #get the result
            result = self.__f(*args,**dargs)
        except Exception:
            #if there is some exception then decrease the trace count by 1
            #then rethrow the Exception
            traced.__count -= 1
            raise ChangeException
            
            
        
        
        #decrease the count on the way back
        traced.__count = traced.__count - 1
        
        #on the way back, we want to print out the pipe again 
        for x in range(self.count()):
            print "| ",
            if(x == self.count() - 1):
                print "`-",
                print repr(result)
                
        # print the last "`- " and the result
        if self.__count == 0:
            print "`-",
            print repr(result)
            return result


        return result

class memoized(object):
    __dList = []
    def __init__(self,f):
        
        #list = {functionName: ([argumentList,result)}
        
        # replace this and fill in the rest of the class
        self.__name__= f.__name__ #assign class name to be function name
        self.__f = f #assign local variable for function
        self.__printString = ""

    #function to reset the dlist
    def reset(self):
        self.__dList = []
        
    def __call__(self,*args,**dargs):
        
        dict = {} #default dictionary
        
        #get all the arguments once the function is called
        argList = []
        for x in args:
            argList.append(x)
        
        #check if its already called
        for x in memoized.__dList:
            try:
                #if it is then we just return the result
                if x[self.__name__][0] == argList:
                    return x[self.__name__][1]
            except:
                pass
        
        #Get the result
        result = self.__f(*args,**dargs)
        
        #dictionary to be added to the list
        dict[self.__name__] = (argList,result)
        
        #append to the global list
        memoized.__dList.append(dict)
        
        return result
    

# run some examples.  The output from this is in decorators.out
def run_examples():
    for f,a in [(fib_t,(7,)),
                (fib_mt,(7,)),
                (fib_tm,(7,)),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (fib_mp.reset,()),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (even_t,(6,)),
                (quicksort_t,([5,8,100,45,3,89,22,78,121,2,78],)),
                (quicksort_mt,([5,8,100,45,3,89,22,78,121,2,78],)),
                (quicksort_mt,([5,8,100,45,3,89,22,78,121,2,78],)),
                (change_t,([9,7,5],44)),
                (change_mt,([9,7,5],44)),
                (change_mt,([9,7,5],44)),
                ]:
        print "RUNNING %s(%s):" % (f.__name__,", ".join([repr(x) for x in a]))
        rv=f(*a)
        print "RETURNED %s" % repr(rv)

@traced
def fib_t(x):
    if x<=1:
        return 1
    else:
        return fib_t(x-1)+fib_t(x-2)

@traced
@memoized
def fib_mt(x):
    if x<=1:
        return 1
    else:
        return fib_mt(x-1)+fib_mt(x-2)

@memoized
@traced
def fib_tm(x):
    if x<=1:
        return 1
    else:
        return fib_tm(x-1)+fib_tm(x-2)

@profiled
@memoized
def fib_mp(x):
    if x<=1:
        return 1
    else:
        return fib_mp(x-1)+fib_mp(x-2)

@traced
def even_t(x):
    if x==0:
        return True
    else:
        return odd_t(x-1)


@traced
def odd_t(x):
    if x==0:
        return False
    else:
        return even_t(x-1)

@traced
def quicksort_t(l):
    if len(l)<=1:
        return l
    pivot=l[0]
    left=quicksort_t([x for x in l[1:] if x<pivot])
    right=quicksort_t([x for x in l[1:] if x>=pivot])
    return left+l[0:1]+right

@traced
@memoized
def quicksort_mt(l):
    if len(l)<=1:
        return l
    pivot=l[0]
    left=quicksort_mt([x for x in l[1:] if x<pivot])
    right=quicksort_mt([x for x in l[1:] if x>=pivot])
    return left+l[0:1]+right

class ChangeException(Exception):
    pass

@traced
def change_t(l,a):
    if a==0:
        return []
    elif len(l)==0:
        raise ChangeException()
    elif l[0]>a:
        return change_t(l[1:],a)
    else:
        try:
            return [l[0]]+change_t(l,a-l[0])
        except ChangeException:
            return change_t(l[1:],a)

@traced
@memoized
def change_mt(l,a):
    if a==0:
        return []
    elif len(l)==0:
        raise ChangeException()
    elif l[0]>a:
        return change_mt(l[1:],a)
    else:
        try:
            return [l[0]]+change_mt(l,a-l[0])
        except ChangeException:
            return change_mt(l[1:],a)


