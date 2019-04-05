from config import pip_number

def calculator(budget, risk):
    #rischio basso
    if risk==0:
        new_budget = (0.01/400)*budget
    #rischio medio
    if risk==1:
        new_budget = (0.01/250)*budget
    #rischio alto
    if risk==2:
        new_budget = (0.01/150)*budget
    
    pip_value = new_budget*0.09*pip
    return pip_value

