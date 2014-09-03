import stackless, select
from socket import *
#   Variables:
lobby_connections = []
address_book = {}
session_connections = []
client_session_index = {}
session_lookup = {}
DSN = 1000 # Default Session Number
go = False # Initilizer Loop variable. (If you get stuff wrong it will remain false till its true)
#   Request Types
JGO = "USV_JGO" # Join Success
JFL = "USV_JFL" # Join Failure
CGO = "USV_"    # Create Success (+ ID to be sent)
CFL = "USV_CFL" # Create Failure


def Central(Pipe,SS,lobby_connections,session_connections,session_lookup,client_session_index):
    while True:
        rlist,wlist,xlist = select.select([SS]+lobby_connections+session_connections,[],[])
        for i in rlist:
            if i == SS:
                socket,address = SS.accept()
                Pipe.send(address)
                Pipe.send("A")
                lobby_connections.append(socket)
                address_book[socket] = address #Add Address Reference

            elif i in lobby_connections:
                try:
                    rq = i.recv(64)
                    if rq:
                        decoded_rq = rq.decode()
                        Pipe.send(i)
                        Pipe.send(rq)
                except Exception as LE:
                    print(LE)

            else:
                # This activity can only be from clients inside sessions, so we need to do some shit.
                # 1: Get the session he is in.
                # 2: Send his message to everyone BUT him.
                number = client_session_index[i] # Got the Session Number
                Session = session_lookup[number] # Now should have a list of sockets.
                try:
                    data = i.recv(4096)
                except Exception as E:
                    data = None
                    i.close()
                    del client_session_index[i]
                    session_connections.remove(i)
                    if i in Session:
                        Session.remove(i)
                    Pipe.send(address_book[i])
                    Pipe.send("K")
                if data:
                    for x in Session:
                        if x != i:
                            try:
                                x.send(data)
                            except Exception:
                                i.close()
                                del client_session_index[i]
                                session_connections.remove(i)
                                if i in Session:
                                    Session.remove(i)
                                Pipe.send(address_book[i])
                                Pipe.send("K")
                    
def Commands(Pipe,DSN,lobby_connections,session_connections,session_lookup,client_session_index): # Prints messages to admin, handles client requests.
    while True:
        item = Pipe.receive()
        command = Pipe.receive()
        try:
            if command == "A":
                print("Client: ",item," joined the Lobby")
        
            elif command == "K":
                print("Client: ",item," was removed from the server")
        
            elif "CS" in str(command[0:2]):
                address = address_book[item]
                print("Client: ",address," made a <Create Session> request")
                item.send((CGO+str(DSN)).encode())
                lobby_connections.remove(item) # Remove him from the lobby
                session_connections.append(item) # Add him to the sessions
                client_session_index[item] = DSN # Add the socket as they key to the number : 1000
                session_lookup[DSN] = [item] # Add (1000: [socket]) As a session
                DSN += 1 # Make DSN 1 higher so that we won't have conflicting problems.
                print("Session: ",(DSN-1)," was created")
    
            elif "JS" in str(command[0:2]):
                address = address_book[item]
                print("Client: ",address," made a <Join Session> request")
                try:
                    ID = int(command[3:])
                except ValueError:
                    print("Client: ",address," sent us fucking letters instead of numbers..")
                    ID = 9999
                if ID in session_lookup:
                    item.send(JGO.encode()) # Send the confirmation
                    lobby_connections.remove(item) # Remove from lobby
                    session_connections.append(item) # Add to sessions list
                    client_session_index[item] = ID # Link him to his session
                    Nodes = session_lookup[ID] # Grab current session list
                    Nodes += [item] # Add him to the list
                    session_lookup[ID] = Nodes # overrwite the old list with the new one
                    print("Client: ",address," Joined Session: ",ID)
                else:
                    print("Client: ",address," has made an invalid request")
                    item.send(JFL.encode())
            else:
                print("Commands Exception: Unknown Command\a")
                print("Commands: Breaking . . .")
                print(command)
                break
        except Exception as E:
            print(E)
            stackless.schedule() # Reschedules itself.
    






print("Stackless IRC Server: Supports Meep 1.2")
host = input("Host: ")
while go != True:
    try:
        port = int(input("Port: "))
        go = True
    except ValueError:
        print("*Your port was invalid*")
        continue
#-------------------------------------------------------------------------------
try:
    SS = socket(AF_INET,SOCK_STREAM)
    SS.bind((host,port))
    SS.listen(2)# Outstanding connections limit.
except IOError:
    print("\nSomething didn't work..")
    input("\nPress Enter to Exit")
Pipe = stackless.channel()
Core = stackless.tasklet(Central)
Core.setup(Pipe,SS,lobby_connections,session_connections,session_lookup,client_session_index)

Subcore = stackless.tasklet(Commands)(Pipe,DSN,lobby_connections,session_connections,session_lookup,client_session_index)
print("Server is now running...\n________________________________________________________")
stackless.run()# Begin Scheduler: (Microthreads will queue up to perform "switches")
