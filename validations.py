

def length_between (value , min, max ): 
    if value is not None and value != "":
        if isinstance(value, int) or isinstance(value, float):
                    value = str(value)
        if not len(value ) >= min and not len(value) < max : 
            return False 
    return True                    


def isRequired(value):
    if value is None or value == "": 
        return  False
    return True    


def isValidStatus (value):
    if value not  in ["failed" , "passed"]:
        return False
    return True         

def TestCaseValidation(data):
    name = data.get("name")  
    description = data.get("description" )
    if(not isRequired(name) ):
        return {"valid": False, "error" : "name is required "} 

    if (not length_between(name , 5  ,20 )):
        return {"valid": False, "error" : "invalid Name length"} 
    if(not isRequired(description) ):
        return {"valid": False, "error" : "description is required "} 

    if (not length_between(description , 5  ,200 )):
        return {"valid": False, "error" : "invalid description length"} 
    

    return {"valid": True} 

def TestCaseExecution(data):
    status = data.get("status")
    if(not isRequired(status) ):
        return {"valid": False, "error" : "status is required "} 

    if (not isValidStatus(status )):
        return {"valid": False, "error" : "invalid status "} 

    return {"valid": True} 


