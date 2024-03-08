#Alexander Kerschen

import os #used to fork a child process
import time #used to make the program sleep
import random #lottery assingment and pull

class Scheduler:
    process_dict = {} #holds the processes to be ran by this scheduler
    
    def add_process(self): #adds a process to the schedule
        a = Process()
        self.process_dict[a.pid] = (a, None) # a is the process, None will be its lottery number after roll_lottery
        
    def roll_lottery(self): #assings all scheduled processes a random lottery number
        taken_values = [] #holds already addinged number to prevent duplicates
        for process, lottery in self.process_dict.values():
            while True:
                num = random.randrange(0, 1000) #random number 0-999
                if num not in taken_values:
                    process.lottery = num #the process itself holds its lottery number
                    self.process_dict[process.pid] = (process, num) #the schedule holds the process next to its lottery number
                    taken_values.append(num)
                    break
                    
    def pull_lottery(self, lottery_tickets):
        return random.choice(lottery_tickets) #picks a random element from the given list of lottery numbers
        
    def run_all_processes(self): #runs a currently scheduled processes in a random order
        self.roll_lottery() #assing the processes lottery numbers
        lottery_dict = {}
        for process, lottery in self.process_dict.values():
            lottery_dict[lottery] = process # make a dictionary where inputing a lottery number returns the corresponding process
        process_num = len(lottery_dict) #holds how many processes need ran
        for x in range(0, process_num): #run every process
            pulled = self.pull_lottery(list(lottery_dict.keys())) #pull a lottery number to determine what process to run next
            pid = os.fork() #create a child process
            if(pid == 0): #if this process is the child process
                self.run_process(lottery_dict[pulled]) #"run" the process
                time.sleep(1.5) #make the program wait 1.5 seconds so everything doesn't just happen super fast
                os._exit(os.getpid()) #terminate the child process
            elif(pid > 0): #if this process is the parent process
                os.wait() #the parent process waits until the child process terminates
            else: #fork() had an error
                print("Proccess failed to start")
            del self.process_dict[lottery_dict[pulled].pid] #remove the process from the scheduled processes
            del lottery_dict[pulled] #remove the process from the processes needing to be ran right now
            
    def run_process(self, process): #"Running" a process
        print(f"Running Process: pid={process.pid}, lottery={process.lottery}")
    

    
class Process:
    pid = 0 #unique identifier of the process
    lottery = 0 #its lottery number
    def __init__(self):
        self.pid = Process.pid
        Process.pid += 1 #increments the static value of pid
        

a = Scheduler()

for x in range (0,5): #makes five processes
    a.add_process()

a.run_all_processes() #run the 5 processes


