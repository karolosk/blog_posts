import time
from timeit import default_timer as timer
from datetime import timedelta

def bubble_sort(elements): 
    elements_length = len(elements) 
  
    # Loop through all elements - essentially the passes 
    for item in range(elements_length): 

        # Loop the list from 0 to item-i-1  
        for i in range(0, elements_length-item-1):
            # Swap if the element found is greater 
            # than the next element 
            if elements[i] > elements[i+1] : 
                elements[i], elements[i+1] = elements[i+1], elements[i]
                # Change the value of control since we had a swap
                # and we need to recheck if there are more to do
        
        
def bubble_sort_optimized(elements): 
    elements_length = len(elements) 
  
    # Loop through all elements - essentially the passes 
    for item in range(elements_length): 
        # Add control
        swapped = False

        # Loop the list from 0 to item-i-1  
        for i in range(0, elements_length-item-1):
            # Swap if the element found is greater 
            # than the next element 
            if elements[i] > elements[i+1] : 
                elements[i], elements[i+1] = elements[i+1], elements[i]
                # Change the value of control since we had a swap
                # and we need to recheck if there are more to do
                swapped = True
        
        # If there were no element swapped 
        # by inner loop, then stop the execution 
        if swapped == False: 
            break

a = [5,2,123,6,900,23,1,6,234,123,0,4]

timer_start = timer() 
bubble_sort(a)
timer_end = timer() 
print(timedelta(minutes=timer_end-timer_start))

timer_start = timer()
bubble_sort_optimized(a)
timer_end = timer() 
print(timedelta(minutes=timer_end-timer_start))

