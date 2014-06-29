import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.config import Config
#_______________________________________________________________________
import os
icon = os.path.abspath("program_data/icon/meep.ico")
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '220')
Config.set ('input', 'mouse', 'mouse,disable_multitouch')
Config.set('kivy', 'window_icon', icon)
Config.set('graphics', 'resizable',1)
#________________________________________________________________________
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.rst import *
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.animation import Animation
from functools import partial
from kivy.clock import Clock
from kivy.core.window import Window
#________________________________________________________________________
from socket import *
import threading
import select
import json
import time
from os.path import *
import math
import winsound
#_________________________________________________________________________
dn = os.path.dirname(os.path.realpath(__file__))
program_assets = os.path.join(dn,"program_data/program_files/program_assets.txt")
hashfile = path = os.path.join(dn,"program_data/program_files/hash.txt")
normal_font = os.path.join(dn,"program_data/fonts/OpenSans-Regular.ttf")
bold_font = os.path.join(dn,"program_data/fonts/OpenSans-Semibold.ttf")
FX = os.path.join(dn,"program_data/sound/blip.wav")
SessionID = None
USERNAME = "Default"
banned = ["yolo","#yolo","swag","#swag"]
Exit = False #Default set to: No Exit.
Primes = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997)
try:
    with open (program_assets, "r") as USERDUMP:
        USERDUMP.close()
except Exception as E:
    IO = open("C:\\nsdump.txt","w")
    IO.write(str(E))
    IO.close()
#_________________________________________________________________________
#_______________________________________________________________________________
# Importing Information

print("Grabbing Username, Seed, and Dictionary")
    
try:
    with open (program_assets, "r") as USERDUMP:
        File = USERDUMP.readlines()
        USERNAME = File[0].rstrip('\n')
        SEED = File[1]
        USERDUMP.close()
       
    if str(SEED) == "None":
        SEED = ""
except NameError:
    USERNAME = ("")
    print("Console: Error encountered loading profile assets")
print("Everything Imported...")
#______________________________________________________________________________
# Defining PRNG Functions
def Primeslist(K): 
    Factors = []
    Denominator = 1
    while Denominator != K:
        Z = K % Denominator
        if Z == 0:
            Factors.append(Denominator)
        Denominator += 1
    return Factors

def Relationsfix(M,M_Factors,C,C_Factors):
    Condition = False
    while Condition != True:
        K = len(M_Factors)
        J = 0
        while J != K:
            if M_Factors[J] in C_Factors and M_Factors[J] != 1:
                M += 1
                M_Factors = Primeslist(M)
                break
            else:
                J += 1
                
        if J == K:
            Condition = True
        else:
            continue
    return M, M_Factors

def Divisrule(M,M_Factors,A,C,C_Factors):
    UU = False
    while UU == False:
        Exceptions = 0
        for i in M_Factors:
            if (A-1)% i == 0:
                print("Divisible.")
            else:
                print("Not divisible")
                Exceptions += 1
        if Exceptions != 0:
            print("Fixing...")
            M = M + 1
            M_Factors = Primeslist(M)
            M, M_Factors = Relationsfix(M, M_Factors, C, C_Factors)
            continue
        else:
            UU = True
            
    return M, M_Factors

def Sequencebuild(A,C,M,X):
    counter = 0
    Sequence = {}
    while counter != M:
        Temp = X
        Sequence[counter] = int(X)
        counter += 1
        X = math.fmod(((A*Temp)+C),M)
        Temp = None
    return Sequence 

def FinalCheck(Sequence):
    Z =Sequence.count(Sequence[1])
    print("Period:",Z)
    if Z > 9:
        print("Fatal")
        return False
    else:
        return True


def Generate(X,A,C,M):
    while C in Primes:
        print("Fixing ",C," to be no longer prime.")
        C += 1
    print(C,": Not prime.")
    # List of Factors for M:
    M_Factors = Primeslist(M)
    print("Factors: ",M_Factors)
    # List of Factors for C
    C_Factors = Primeslist(C)
    print("Factors: ",C_Factors)
    # Now we need to make sure they are relatively prime.
    # We AREN'T changing the users input, so only M + M_Factors will be altered.
    M, M_Factors = Relationsfix(M,M_Factors,C,C_Factors)
    print("Number: ",M," with factors: ",M_Factors," is relatively prime to: ",C," with factors: ",C_Factors)
    M, M_Factors = Divisrule(M,M_Factors,A,C,C_Factors)
    print("Number: ",M," with factors: ",M_Factors," is relatively prime to: ",C," with factors: ",C_Factors)
    Sequence = Sequencebuild(A,C,M,X)
    N = FinalCheck((list(Sequence.values())))
    if N == False:
        return A.Show_Popup(Type = "ErrorPopup",Text = "Corruption Error\nTry a new seed",rq = True)
    Sequence_Stripped = list(Sequence.values())

    Letters_lower = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
    Space = tuple(" ")
    Letters_upper = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z")
    Numbers = ('1','2','3','4','5','6','7','8','9','0')
    Specials = ('~','`','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|',':',';','"',"'",',','<','.','>','/','?','!')
    Combined = Letters_lower + Space + Letters_upper + Numbers + Specials
    print("\n\n",Combined)
    print("Making a Dictionary...")
    #-----------------
    Cryptdict = {}
    RP = len(Combined)
    RC = 0
    while RC != RP:
        Cryptdict[Sequence_Stripped[RC]] = Combined[RC]
        RC += 1
    print(Cryptdict)
    try:
        with open(hashfile,"w") as O:
            json.dump(Cryptdict,O)
            O.close()
            print("Wrote to file.")
    except IOError as Error:
        print(Error)
        return A.Show_Popup(Type = "ErrorPopup",Text = "File Error\nCouldn't locate crypt.dat",rq = True)

def Call(Raw_Seed):
    A = App.get_running_app()
    global Seed
    FatalList = [512,256,128]
    Seed = Raw_Seed[:9]
    if "000" in Seed:
        print("\a\a")
        return A.Show_Popup(Type = "ErrorPopup",Text = "Too many zeroes in seed\nNo more than 2",rq = True)
    X = int(Seed[:3])
    A = int(Seed[3:6])
    C = int(Seed[6:9])
    if C in FatalList:
        C += 1
    M = 1024 # Default Period Length
    Generate(X,A,C,M)
    return

#______________________________________________________________________________
# Defining General Program Functions

def username_update(username,screen_reference,seed):
    global USERNAME
    print("Function: Updating Username")
    screen_reference.usn.text = username
    with open (program_assets, "w") as File:
        File.write(username + "\n" + seed)
        File.close()
        USERNAME = username
        print("Username Updated")
    return


def seed_update(seed,screen_reference, username):
    global SEED
    print("Function: Updating Seed and Dictionary")
    Call(seed)
    with open (program_assets, "w") as File:
        File.write(username + "\n" + seed)
        File.close()
        SEED = seed
        print("Seed Updated")
    pass
#______________________________________________________________________________
     
def Auto(S): # Receiving Thread. Handles all message receival. 
    A = App.get_running_app()
    print("Mainloop Beginning . . . ")
    print("> Loading Files . . . ")
    with open(hashfile,"r") as F:
        N = json.load(F)
        global R_Dictionary
        R_Dictionary = dict(N)
        print("R_Dictionary:",R_Dictionary)
        F.close()
    global T_Dictionary
    T_Dictionary = {}
    for key,val in R_Dictionary.items():
        T_Dictionary[val] = key
    print("T_Dictionary:",T_Dictionary)
    rlist,wlist,xlist = select.select([S],[],[])
    print(" > Listening . . . ")
    while True:
        if Exit == True:
            print("Exit Call: Breaking")
            break
        else:
            for i in rlist:
                try:
                    Flag = i.recv(4)
                    try:
                        Data = i.recv(int(Flag.decode()))
                    except ValueError:
                        Data = ""
                except OSError:
                    print("Auto: Returning >")
                    return
                if Data:
                    try:
                        Processed_Data = json.loads(Data.decode())
                    except StopIteration:
                        A.Show_Popup("ErrorPopup","StopIteration Error\nRecommended restart",True)
                    V = 0
                    C = len(Processed_Data)
                    decrypted_data = []
                    while V != C:
                        try:
                            decrypted_data += [R_Dictionary[Processed_Data[V]]]
                            V += 1
                        except KeyError as EError:
                            A.Command(A.screenmanager.current_screen,"k")
                            print(EError)
                            V = C
                    Message = "".join(str(W) for W in decrypted_data)
                    Split = Message.split(":")
                    Recombined = "[color=#004C99]"+Split[0]+ ": "+"[/color]" + "".join(F for F in Split[1:])
                    if "@"+USERNAME in Message:
                        Beep(FX)
                        Q = SpecLabel()
                        Q.color_rgba = (1,.2,.2,.3)
                        A.screenmanager.current_screen.chat_grid.add_widget(Label(size_hint = (None,None),size = (300,10)))
                        A.screenmanager.current_screen.chat_grid.add_widget(Q)
                        Q.text = " " + Message
                        Q.size = Q.texture_size
                        Q.halign = 'left'
                        Q.valign = 'top'
                    else:
                        Q = ChatLabel()
                        Q.color_rgba = (1,1,1,0)
                        A.screenmanager.current_screen.chat_grid.add_widget(Label(size_hint = (None,None),size = (300,10)))
                        A.screenmanager.current_screen.chat_grid.add_widget(Q)
                        Q.text = " " + Recombined
                        Q.size = Q.texture_size
                        Q.halign = 'left'
                        Q.valign = 'top'
    print("Auto: Returned.")
        
def Beep(sound):
    winsound.PlaySound(sound, winsound.SND_FILENAME)
    
def ExternalConnect(S, host):
    app = App.get_running_app()
    try:
        S.connect((host,9090))
        global H
        H = S.getpeername()
        return app.LP.dismiss(), app.Show_Popup("OptionPopup",str(H[0]).strip("'"),True)
    
    except Exception as F:
        print(F)
        return app.LP.dismiss(), app.Show_Popup("ErrorPopup","Either..\n1: No Response\n2: Refused Connection",True)

        
def squak(socket,request,screen):
    global SessionID
    app = App.get_running_app()
    try:
        socket.send(request.encode())
        RT = socket.recv(64)
        R = str(RT.decode())
        print(R)
        if R == "USV_JGO":
            SessionID = request[3:]
            print("Successfully Joined Session: " + str(SessionID))
            app.screenmanager.current = "ChatScreen"
            return threading.Thread(target= Auto, args = (socket,)).start()
        elif R == "USV_JFL":
            app.Show_Popup("OptionPopup",str(H[0]).strip("'"),True)
            app.Show_Popup("ErrorPopup","No such Session",True)
                
        elif len(R) == 8:
            print("Successfully Created Session: " + R[4:])
            SessionID = R[4:]
            screen.dismiss()
            app.screenmanager.current = "ChatScreen"
            return threading.Thread(target= Auto, args = (socket,)).start()
        else:
            app.Show_Popup("ErrorPopup","Server could not create\nthe session",True)
                
    except Exception as I:
        print(I)
        app.Show_Popup("ErrorPopup","Connection to host lost",True)        
    
#_________________________________________________________________________
kv = """
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import Window kivy.core.window.Window

<Menu>:
    host: host_input
    seed: None
    usn: userid_input
    on_pre_enter: app.InfoBuild(self)
    b1: a
    b2: b
    b3: c
    b4: d
    b5: e
    b6: f
    b7: g
    b8: h
    b9: i
    BoxLayout:
        cols: 1
        orientation: 'vertical'
        spacing: 10
        size: self.size
        pos: self.pos
        
        canvas.before:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: self.pos
                size: self.size
                
        Label:
            font_name: app.menu_font
            text: "[color=#000000]Meep[/color][color=#003368][sub] 1.3.5[/sub][/color]"
            markup: True
            size_hint: .5,None
            height: self.texture_size[1]
            pos_hint: {'x':.25,'y':.9}
            valign: 'top'
            font_size: 25        

        GridLayout:
            cols: 2
            size_hint_x: None
            width: self.minimum_width
            spacing: 5
            canvas:
                Color:
                    rgba: 1,1,1,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                font_name: app.menu_font
                text: "Host: "
                valign: 'top'
                font_size: 15
                size_hint: None,None
                height: 30
                width: 70
                background_color: 1,.5,0,1
                color: 0,0,0,.8

            TextInput:
                font_name: app.menu_font
                canvas.before:
                    Color:
                        rgba: 0,.2,.4,.8
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    Color:
                        rgba: 1,1,1,1
                id: host_input
                font_size: 15
                cursor_blink: False
                hint_text: 'Address'
                size_hint: None,None
                height: 35
                width: 250
                multiline: False
                background_color: 1,1,1,0
                valign: 'top'
                on_text_validate: app.Launch(root.host.text,root.usn.text,root)

            Label:
                font_name: app.menu_font
                text: "Seed: "
                valign: 'top'
                font_size: 15
                size_hint: None,None
                height: 30
                width: 70
                background_color: 1,1,1,1
                color: 0,0,0,.8

            BoxLayout:
                orientation: "horizontal"
    
                StackLayout:
                    orientation: 'lr-tb'
                    padding: 0
                    spacing: [.5,0]
                    canvas:
                        Color:
                            rgba: 1,1,1,0
                        Rectangle:
                            pos: self.pos
                            size: self.size

                    TextInput:
                        id: a            
                        canvas.before:
                            Color:
                                rgba: 0,.2,.4,.8
                            Rectangle:
                                pos: self.pos
                                size: self.size
                            Color:
                                rgba: 1,1,1,1
                    
                        on_focus: app.setup(root), print("TextInput: Now focused.")
                        text: ""
                        size_hint: None, None
                        font_name: app.menu_font
                        multiline: False
                        height: 30
                        width: 27

                    TextInput:
                        id: b

                        canvas.before:
                            Color:
                                rgba: 0,.2,.4,.8
                            Rectangle:
                                pos: self.pos
                                size: self.size
                            Color:
                                rgba: 1,1,1,1
                    
                        readonly: True
                        text: ""
                        size_hint: None, None
                        font_name: app.menu_font
                        multiline: False
                        height: 30
                        width: 27

                    TextInput:
                        id: c

                        canvas.before:
                            Color:
                                rgba: 0,.2,.4,.8
                            Rectangle:
                                pos: self.pos
                                size: self.size
                            Color:
                                rgba: 1,1,1,1
                    
                        readonly: True
                        text: ""
                        multiline: False
                        size_hint: None, None
                        font_name: app.menu_font
                        height: 30
                        width: 27               

        
                    TextInput:
                        id: d

                        canvas.before:
                            Color:
                                rgba: 0,.2,.4,.8
                            Rectangle:
                                pos: self.pos
                                size: self.size
                            Color:
                                rgba: 1,1,1,1
                    
                        readonly: True
                        text: ""
                        multiline: False
                        size_hint: None, None
                        font_name: app.menu_font
                        height: 30
                        width: 27

                    TextInput:
                        id: e

                        canvas.before:
                            Color:
                                rgba: 0,.2,.4,.8
                            Rectangle:
                                pos: self.pos
                                size: self.size
                            Color:
                                rgba: 1,1,1,1
                    
                        readonly: True
                        text: ""
                        multiline: False
                        size_hint: None, None
                        font_name: app.menu_font
                        height: 30
                        width: 27

                    TextInput:
                        id: f

                        canvas.before:
                            
                            Color:
                                rgba: 0,.2,.4,.8
                            Rectangle:
                                pos: self.pos
                                size: self.size
                            Color:
                                rgba: 1,1,1,1
                    
                        readonly: True
                        text: ""
                        multiline: False
                        size_hint: None, None
                        font_name: app.menu_font
                        height: 30
                        width: 27

                    TextInput:
                        id: g

                        canvas.before:
                            Color:
                                rgba: 0,.2,.4,.8
                            Rectangle:
                                pos: self.pos
                                size: self.size
                            Color:
                                rgba: 1,1,1,1
                    
                        readonly: True
                        text: ""
                        multiline: False
                        size_hint: None, None
                        font_name: app.menu_font
                        height: 30
                        width: 27

                    TextInput:
                        id: h

                        canvas.before:
                            Color:
                                rgba: 0,.2,.4,.8
                            Rectangle:
                                pos: self.pos
                                size: self.size
                            Color:
                                rgba: 1,1,1,1
                    
                        readonly: True
                        text: ""
                        multiline: False
                        size_hint: None, None
                        font_name: app.menu_font
                        height: 30
                        width: 27
            
                    TextInput:
                        id: i

                        canvas.before:
                            Color:
                                rgba: 0,.2,.4,.8
                            Rectangle:
                                pos: self.pos
                                size: self.size
                            Color:
                                rgba: 1,1,1,1
                    
                        readonly: True
                        text: ""
                        multiline: False
                        size_hint: None, None
                        font_name: app.menu_font
                        height: 30
                        width: 27  
                
            Label:
                font_name: app.menu_font
                text: "User ID: "
                valign: 'top'
                font_size: 15
                size_hint: None,None
                height: 30
                width: 80
                background_color: 1,1,1,1
                color: 0,0,0,.8

            TextInput:
                font_name: app.menu_font
                canvas.before:
                    Color:
                        rgba: 0,.2,.4,.8
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    Color:
                        rgba: 1,1,1,1
                id: userid_input
                font_size: 15
                cursor_blink: False
                hint_text: '15 character limit'
                size_hint: None,None
                height: 35
                width: 240
                multiline: False
                background_color: 1,1,1,0
                valign: 'top'
                
        Button:
            font_name: app.menu_font
            canvas:
                Color:
                    rgba: 0,.3,.6,.4
                Rectangle:
                    size: self.size
                    pos: self.pos
            text: "Link"
            size_hint: .4,.25
            pos_hint: {'x':.3,'y':.2}
            height: 30
            background_color: .2,.4,1,0
            color: 0,0,0,.9
            on_press:
                app.Launch(root.host.text,root.usn.text,root)
                
    
    
        Label:
            font_name: app.menu_font
            text: "Created by Owatch"
            valign: 'top'
            font_size: 12
            size_hint: None,.25
            pos_hint: {'x':0,'y':.05}
            height: 50
            width: 200
            background_color: 1,1,1,1
            color: 0,0,0,.6
            
<ErrorPopup>:
    ref: b
    size_hint: None, None
    size: 200,150
    title: "Error"
    title_color: [1,1,1,1]
    auto_dismiss: True
    separator_color: [1,1,1,1]
    Label:
        id: b
        text: "None"
        font_name: app.menu_font
        background_color:[1,1,1,1]

<LoadingPopup>:
    ref: b
    on_open:
    size_hint: None, None
    size: 200,150
    title: "Awaiting reply . . . "
    title_color: [1,1,1,1]
    auto_dismiss: False
    separator_color: [0,.129,.258,1]
    Label:
        post_hint: {'x':.104,'y':.063}
        font_name: app.menu_font
        font_size: 30
        id: b
        text: ""
        background_color:[1,1,1,1]

<OptionPopup>:
    ref: z
    size_hint: None, None
    size: 300,200
    title: "Client Options"
    title_color: [1,1,1,1]
    separator_color: [0,.129,.258,1]
    GridLayout:
        spacing: 3
        cols: 1
        Label:
            id: z
            markup: True
        Button:
            canvas:
                Color:
                    rgba: 1,1,1,.5
                Rectangle:
                    size: self.size
                    pos: self.pos
            text: "Create Session"
            background_color:[.1,.1,.1,1]
            on_release: app.query("CS_####",root)
        Button:
            canvas:
                Color:
                    rgba: 1,1,1,.5
                Rectangle:
                    size: self.size
                    pos: self.pos
            text: "Join Session"
            background_color:[.1,.1,.1,1]
            on_release: app.Show_Popup("IDPopup","",True), root.dismiss()
        Button:
            canvas:
                Color:
                    rgba: 1,.5,.5,.5
                Rectangle:
                    size: self.size
                    pos: self.pos
            text: "Abort"
            background_color:[.9,.1,.1,1]
            on_release: root.dismiss(), app.S.close()
<IDPopup>:
    ref: k
    size_hint: None, None
    size: 95,100
    title: "ID Code"
    title_color: [1,1,1,1]
    auto_dismiss: True
    separator_color: [1,1,1,1]
    TextInput:
        id: k
        font_size: 20
        hint_text: "####"
        foreground_color:[.4,.4,1,1]
        background_color:[.2,.2,.2,.7]
        multiline: False
        on_text_validate:
            app.query("JS_" + self.text, None)
            root.dismiss()

            
<ChatScreen>:
    entry_drop: entry_input
    chat_grid: grid_input
    BoxLayout:
        size: self.size
        pos: self.pos
        orientation: 'vertical'
        spacing: 4

        canvas:
            Color:
                rgba: 0,.129,.258,1
            Rectangle:
                pos: self.pos
                size: self.size           


        ScrollView:
            canvas.before:
                Color:
                    rgba: .95,.95,.95,1
                Rectangle:
                    pos: self.pos
                    size: self.size

            
            GridLayout:
                id: grid_input
                canvas:
                    Color:
                        rgba: .95,.95,.95,1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                cols: 1
                size_hint_y: None
                height: self.minimum_height

        TextInput:
            id: entry_input
            font_name: app.menu_font
            text: ""
            multiline: False
            hint_text: "                                     Enter to Send"
            focused: True
            foreground_color: 1,1,1,1
            padding: (4,1)
            border: 0,0,0,0
            background_color: 1,1,1,0
            size_hint: 1,0.08
            on_text_validate: app.Process(root,self.text)
            
<ChatLabel>:
    size_hint: (None,None)
    text_size: (350,None)
    markup: True
    font_name: app.menu_font
    size: (350,self.texture_size[1])
    color: 0,0,0,1
    text: " "
    canvas:
        Color:
            rgba: root.color_rgba
        Rectangle:
            pos: self.pos
            size: self.size
<SpecLabel>:
    size_hint: (None,None)
    text_size: (350,None)
    markup: True
    font_name: app.menu_font
    size: (350,self.texture_size[1])
    color: 0,0,0,1
    text: " "
    canvas:
        Color:
            rgba: root.color_rgba
        Rectangle:
            pos: self.pos
            size: self.size
"""
Builder.load_string(kv)

class Menu(Screen):
    def on_pre_enter(self):
        Window.size=(400,250)
    def on_leave(self):
        pass
    
class ErrorPopup(Popup):
    pass

class OptionPopup(Popup):
    pass

class LoadingPopup(Popup):
    pass

class IDPopup(Popup):
    pass

    

class ChatLabel(Label):
    color_rgba = ListProperty([0,0.298,0.6,0])
    
class SpecLabel(Label):
    color_rgba = ListProperty([0,0.298,0.6,0])

class ChatScreen(Screen):
    def on_pre_enter(self):
        self.chat_grid.bind(height = self.ScrollControl)
        Window.size=(400,500)
    def on_enter(self):
        app = App.get_running_app()
        app.Process(self,">session")
        app.Send(" joined the session",True)
    def on_leave(self):
        self.chat_grid.clear_widgets()
        global Exit
        Exit = True
        print("Closed socket, exited ChatScreen.")
        
    def ScrollControl(self,*args):
                   self.chat_grid.parent.scroll_y = 0

class Meep(App):
    menu_font = normal_font
    
    def setup(self,root):
        self.Boxes = {1: root.b1, 2: root.b2, 3: root.b3,4: root.b4, 5: root.b5, 6: root.b6, 7: root.b7, 8: root.b8, 9: root.b9}
        self.base = 1
        print("SETUP: I should only be called once.")
        self.Boxes[self.base].text = ""
        root.b1.focus = False
        self.keyboard = Window.request_keyboard(callback = self.delink ,target = self.Boxes[self.base], input_type = "text")
        self.keyboard.bind(on_key_up = self.validate)

    def delink(self):
        print("Keyboard Delinked")
        try:
            self.keyboard.unbind(on_key_up = self.validate)
            self.keyboard = None
        except AttributeError:
            print("ATTRIBUTE ERROR") # Show Popup

    def validate(self,a,b):
        print("Validate: I should only be called once")
        try:
            int(b[1])
            self.Boxes[self.base].text = b[1] # b is a tuple, 1 is the key pressed
            self.Boxes[self.base].on_text_validate()
            self.Boxes[self.base].readonly = True
        except ValueError:
            self.Boxes[self.base].text = ""
            return self.Show_Popup("ErrorPopup","Integers Only",True)
        

        self.base = self.base + 1
        if self.base == 10:
            self.keyboard.unbind(on_key_up = self.validate)
            self.keyboard = None
        else:
            self.Boxes[self.base].readonly = False
            self.keyboard = Window.request_keyboard(callback = self.delink ,target = self.Boxes[self.base], input_type = "text")
            self.keyboard.bind(on_key_up = self.validate)
            
    def InfoBuild(self,screen):
        screen.usn.text = USERNAME
        elements = [i for i in SEED]
        screen.b1.text = elements[0]
        screen.b2.text = elements[1]
        screen.b3.text = elements[2]
        screen.b4.text = elements[3]
        screen.b5.text = elements[4]
        screen.b6.text = elements[5]
        screen.b7.text = elements[6]
        screen.b8.text = elements[7]
        screen.b9.text = elements[8]
        
    def Show_Popup(self,Type,Text,rq): #rq just determines whether it is dismissable by clicking outside the box. True = yes, False = no
        T = {"ErrorPopup":ErrorPopup,"OptionPopup":OptionPopup,"IDPopup":IDPopup,"LoadingPopup":LoadingPopup}
        F = T[Type]
        L = F().open()
        if rq == False:
            return
        L.ref.text = Text

    def Launch(self,host,username,screen):
        global Exit
        Exit = False
        screen_reference = screen
        seed = screen.b1.text + screen.b2.text + screen.b3.text + screen.b4.text + screen.b5.text + screen.b6.text + screen.b7.text + screen.b8.text + screen.b9.text
        if username != USERNAME:
            username_update(username,screen_reference,seed)
        if seed != SEED:
            if len(seed) != 9:
                self.Show_Popup("ErrorPopup","Seed must be 9\ncharacters long",True)
                return
            else:
                seed_update(seed,screen_reference,username)
        self.Connect(host) # Creates a thread to handle the connection without interrupting main.
        
    def Connect(self,host):
        self.S = socket(AF_INET,SOCK_STREAM)
        self.LP.open()
        threading.Thread(target = ExternalConnect, args =(self.S,host)).start()
   
    def Command(self,screen,order):
        if order == "t":
            X = "[i]"+time.asctime(time.localtime(time.time()))+"[/i]"
            screen.chat_grid.add_widget(Label(size_hint = (None,None),size = (300,10)))
            screen.chat_grid.add_widget(Label(text = X, color = (0,0,0,1),valign='middle',font_name = bold_font, markup= True, size_hint = (None,None),size = (300,20)))
            
        elif order == "#":
            X = "[i]"+"Current Session: "+"[color=ff8000]"+str(SessionID)+"[/color]"+"[/i]"
            screen.chat_grid.add_widget(Label(size_hint = (None,None),size = (300,10)))
            screen.chat_grid.add_widget(Label(text = X, color = (0,0,0,1),valign='middle',font_name = normal_font, markup= True, size_hint = (None,None),size = (300,20)))
            
        elif order == "h":
            X = "Display Time: "+"[color=ff8000]>time[/color]"+"\n"+"Display Session: "+"[color=ff8000]>session[/color]"+"\n"+"Notify a User: "+ "[color=ff8000]@[/color]"+"[color=000099]username[/color]"+"\n"+"Exit to Menu: [color=ff8000]>exit[/color]"
            screen.chat_grid.add_widget(Label(size_hint = (None,None),text="Commands",color = (0,0,0,1),font_name = bold_font,size = (300,20)))
            screen.chat_grid.add_widget(Label(text = X, color = (0,0,0,1),font_name = normal_font,valign='middle',markup= True, size_hint = (None,None),size = (300,100)))
            
        elif order == "k":
            X = "[color=ff0000]Received Unfamiliar Data[/color]"
            screen.chat_grid.add_widget(Label(size_hint = (None,None),text="Warning",color = (1,0,0,1),font_name = bold_font,size = (300,20)))
            screen.chat_grid.add_widget(Label(text = X, color = (0,0,0,1),font_name = normal_font,valign='middle',markup= True, size_hint = (None,None),size = (300,20)))
            
        elif order == "x":
            self.Send(" left the session",True)
            self.S.close()
            self.screenmanager.current = "Menu"
            
            

    def Process(self,screen,message):
        
        if str(message).strip(' ')== ">time":
            self.insert(screen,None)
            self.Command(screen,"t")
            return
        elif str(message).strip(' ') == ">session":
            self.insert(screen,None)
            self.Command(screen,"#")
            return
        elif str(message).strip(' ') == ">help":
            self.insert(screen,None)
            self.Command(screen,"h")
            return
        elif str(message).strip(' ')== ">exit":
            self.insert(screen,None)
            self.Command(screen,"x")
            return
        elif message == "":
            return
        for i in banned:
            if i in message:
                message = "*Obscenity Prevented*"
        self.Send(message,False)
        self.insert(screen,message)

    def Send(self,message,sort):
        if sort == True:
            package = "** "+ USERNAME + message + " **:"
        else:
            package = USERNAME + ": " + str(message)
        List = []
        Counter = 0
        Stop = len(package)
        while Counter != Stop:
            try:
                List += [T_Dictionary[package[Counter]]]
                Counter += 1
            except KeyError:
                Counter = Stop
                return self.Show_Popup("ErrorPopup","Something in the message\ncan't be encrypted")
        Mail = json.dumps(List)
        try:
            size = str("%04d" % (len(Mail),))
            self.S.send((size+Mail).encode())
            print("Sent: ",(size+Mail))
        except Exception:
            self.Show_Popup("ErrorPopup","Connection Lost\nPlease Reconnect",True)
            return
        

    def insert(self,screen,message):
        if message == None:
            Clock.schedule_once(partial(self.scheduled_screen_focus,screen))
            return
        Temp = ChatLabel()
        screen.chat_grid.add_widget(Label(size_hint = (None,None),size = (300,10)))
        screen.chat_grid.add_widget(Temp)
        Temp.text = "[color=#FF8000][b]"+" "+USERNAME+":  "+"[/b][/color]" +"[color=#000000]"+ message +"[/color]"
        Temp.size = Temp.texture_size
        Temp.halight = "left"
        Temp.valight = "top"
        Clock.schedule_once(partial(self.scheduled_screen_focus,screen))
        
    def query(self,request,screen):
        threading.Thread(target = squak, args = (self.S,request,screen)).start()
        
        
    def scheduled_screen_focus(self,screen,dt):
        widget = screen.entry_drop
        widget.select_all()
        widget.delete_selection()
        widget.focus = True
        
    def Screen(self):
        Screen = kivy.uix.screenmanager.Screen
        Window.size =(400, 220)
        
    def build(self):
        self.LP = LoadingPopup()
        self.screenmanager = ScreenManager(transition=SlideTransition())
        self.screenmanager.add_widget(Menu(name='Menu'))
        self.screenmanager.add_widget(ChatScreen(name='ChatScreen'))

        return self.screenmanager

    def on_stop(self):
        try:
            global Exit
            Exit = True
            self.S.close()
        except Exception as I:
            print(I)
            
if __name__ == "__main__":
    Meep().run()
    
                
