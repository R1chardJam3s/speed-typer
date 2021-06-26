import socket #used to connect computers
import threading #allows threaded clients so multiple clients can connect to the server in one go
import random #import for random sentenc generation
import pickle #used for string serialisation for a array so it can be passed between files

#create arrays that are used through the program
times = [] #times sorted in this list
names = [] #list of names for users connected

#list of singular nouns used
s_nouns = ["A dude", "My mom", "The king", "Some guy",\
    "A cat with rabies", "A sloth", "Your homie", "Superman"]

#list of singular verbs used
s_verbs = ["eats", "kicks", "gives", "treats",\
    "meets with", "creates", "hacks", "configures",\
    "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]

#random phrase generation code
def getPhrase():
    phrase = random.choice(s_nouns) + " " + random.choice(s_verbs) + " " + random.choice(s_nouns).lower()
    return phrase

#compares the times that the connected users take to complete sentence
def compare():
    cTimes = [] #holds the times taken for the users, if they completed the sentence correctly
    for i in range(len(times)): #for length of times array
        if times[i][1] != "False": #if they did get it correct, it appends it to cTimes
            cTimes.append(times[i][1]) #append time
    cTimes = sorted(cTimes) #sort the list in order
    print("Sorted:",cTimes) #print sorted list
    for i in range(lobby_size): #for loop to run however big the lobby is
        if times[i][1] == cTimes[0]: #if the time is the fastest
            return str(times[i][0]) #return the winner and break

#connectUser subroutine. Runs each time a client connects to the server
def connectUser():
    server_socket.listen(1) #list for a connection
    conn, addr = server_socket.accept() #accept the connection
    print("Connection from:",addr) #print statement to clarify connection
    conn.send("Connected".encode()) #send "Connected" to client, gets rid of a false connection error
    conn.send(str(lobby_size).encode()) #send lobby_size to user
    name = conn.recv(1024).decode() #recieve the name from the client
    names.append(name) #append the name to the global names array
    print(name,"has connected via port",addr[1]) #clarify the user has connected

    #sends lobby to players when all have connected
    while True:
        if len(names) == lobby_size: #if everyone has connected
            data = pickle.dumps(names) #serialise the array into 'data'
            conn.send(data) #send data
            break #break out of while loop

    #acts as a halt so the user has to press enter to continue. Otherwise it will send the phrase before the client is ready to recieve
    conn.recv(1024)

    conn.send(phrase.encode()) #encode and send the phrase
    timeTaken = conn.recv(1024).decode() #recienve time taken calculated from client
    print("It took",name,str(timeTaken),"seconds") #print how long it took the user to complete
    Time = [name,timeTaken] #use 'Time' to append the name and time taken to 'times' in a 2d array
    times.append(Time) #append Time to 'times'
    print(times) #print times
    while True: #while to loop to ensure everyone has completed the phrase
        if len(times) == lobby_size: #if everyone has completed
            break #break out of the while loop
    winner = compare() #calculate and recieve the winner

    #send winner to the clients
    conn.send(winner.encode())
    
#main program start
while True:
    try: #try except to validate lobby size
        lobby_size = int(input("Enter desired lobby size (max 4): "))
    except ValueError: #except ValueError
        print("Enter a value")
    else:
        if lobby_size >= 1 and lobby_size <= 4: #if lobby size is in range
            break #break
        else:
            print("Enter a lobby size in range 1-4")

#set host and user defined port
host = socket.gethostbyname(socket.gethostname())
port = int(input("Enter port: "))

#create socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((host, port)) #bind host and port to socket

#print host and port for validation
print(host,port)

#generate phrase
phrase = getPhrase()

 
#for loop runs for desired lobby size
for i in range(lobby_size):
    connection_thread = threading.Thread(target = connectUser) #create a thread everytime a client connects to the server
    connection_thread.start() #start the thread 






