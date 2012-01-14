from misc import Failure

class Vector(object):

    myList = [] #init a list
    
    def __init__(self,arg):
        self.myList = []
        #IF int or long or float then initiate array of 0.00 with the args as the size
        if(type(arg) == int or type(arg) == long or type(arg) == float):
            aNum = int(arg) #checking the type
            if(aNum < 0): #If less than - then raise value error
                raise ValueError("Vector length cannot be negative")
            else:
                for i in range(aNum):
                    self.myList.append(0.0) #otherwise just loop through and append to list
        else: 
            try:
                #if it's a sequence then turn each of the element into the list
                for x in arg:
                    self.myList.append(x)
            except:
                #otherwise raise typeerror
                raise TypeError("Sequence or int/long only")
                    

    def __repr__(self):
        returnString = '' #initializer
        i = len(self.myList)
        #go through each element inside the list
        for x in self.myList:
            if (type(x) == str):
                #add each of the list element into the string
                returnString += "'" + x + "'"
            else:
                returnString += str(x)
            #this code is to check so we don't have the extra comma at the end
            if(i != 1):
                returnString += ', '
            i = i - 1
        #return the string element with Vector as outer loop
        return "Vector([" + returnString + "])"
    
    def __len__(self):
        #count how many element inside the Vector.
        count = 0;
        for x in self.myList:
            count += 1
        return count

    def __iter__(self):
        #iterate through each item and yield it
        for x in self.myList:
            yield x
            
    def __add__(self, other):
        resultList = []
        #for loop through 2 items at the same time and add the element together
        for x,y in zip(self,other):
            resultList.append(x+y)
        return Vector(resultList)
            
    def __radd__(self, other):
        #add only work when we add 2 lists/Vector together so we have to worry
        #about other sequence; hence, radd is needed
        resultList = []
        for x,y in zip(self,other):
            resultList.append(x+y)
        return Vector(resultList)
    
    def dot(self,other):
        result = 0 #set it equal to zero
        for x,y in zip(self,other):
            result += x*y #equation to find the dot product
        return result
    
    def __getitem__(self,index):
        #if its a slice then we just get the slices
        if(type(index) != int):
            return self[index]
        else:
            #if its out of bound then we raise indexerror
            if(index >= len(self)):
                raise IndexError("Array Index Out Of Bound In Get Item")
            else:
                #otherwise we just return the elements inside the list
                vectorLength = len(self)
                if(index < 0):
                    index += vectorLength
                return self.myList[index]
                
    def __setitem__(self,index,value):
        #if its a slice then we just set it
        if(type(index) != int):
            self[index] = value
        else:
            #statement to check and make sure the length is nothing being modified
            if(index >= len(self)):
                raise IndexError("Array Index Out Of Bound In Set Item")
            else:
                #otherwise we just go through and set the Vector equal to the value
                vectorLength = len(self)
                if(index < 0):
                    index += vectorLength
                self.myList[index] = value
    
    #Check if two things are equal  
    def __eq__(self,other):
        #if the type is not equal then we can return False or compare the Vector with other element
        if type(other) != Vector:
            return (other == self.myList)
        else:
            #boolean which we will return
            returnBoolean = False;
            #go through each element of the two list
            #if they are the same through out then set returnboolean to be true
            #as soon as one of them is not equal then return false instantly
            for x,y in zip(self, other):
                if x == y:
                    returnBoolean = True
                else:
                    return False
        return returnBoolean
    
    def __gt__(self,other):
        #if the type is not equal then we can return False or compare the Vector with other element
        if type(other) != Vector:
            return (other <= self.myList)
        else:
            #assume the first element of each list is the largest element
            largestSelf = self[0]
            largestOther = other[0]
            #start checking if its the largest element
            #if it is then set it to be the largest element
            for x in self:
                if x > largestSelf:
                    largestSelf = x
                    
            #Same check for other like self
            for x in other:
                if x > largestOther:
                    largestOther = x
            
            #then we check if largestSelf is bigger than largestOther   
            return (largestSelf > largestOther)
        
    def __lt__(self,other):
        #if the type is not equal then we can return False or compare the Vector with other element
        if(type(other) != Vector):
            return (other >= self.myList)
        else:
            #use what we have so far to check for less than
            if(self > other or self >= other):
                return False
            else:
                return True
    
    def __ge__(self,other):
        #if the type is not equal then we can return False or compare the Vector with other element
        if type(other) != Vector:
            return (other < self.myList)
        while(len(self) != 0 or len(other) != 0):
            #assume the first element of each sequence is the bigget number
            lSelf = self[0]
            lOther = other[0]
            #if it is then set it to be the largest element
            for x in self:
                if x > lSelf:
                    lSelf = x
            #remove it from the list
            self.myList.remove(lSelf)
            
            #find the bggest element in the Other seuqnce
            #if it is then set it
            #then remove it from the list
            for x in other:
                if x > lOther:
                    lOther = x
            other.myList.remove(lOther)
            
            #if they are not equal then return false
            if(lSelf != lOther):
                return False
            
        return True

