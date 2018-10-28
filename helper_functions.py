def text_len(text):
  textLength = len(text)

  if textLength < 3:
    return False

  else:
    return True

def no_spaces(text):
  
  if ' ' in text:
    return False
  else:
    return True


def input_validation(input):
    
  if text_len(input) and no_spaces(input) == True:
      
    return True
  else:
  
    return False
    
def password_match(password, passwordConfirmation):
    if passwordConfirmation == '':
        return False 
    
    elif password == passwordConfirmation:
        return True   

    else:
        return False 
  
    