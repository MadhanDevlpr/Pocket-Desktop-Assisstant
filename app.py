import sys
import wikipedia
import os
import pyautogui as pg
import datetime
import time as ts
import speech_recognition as sr 
import webbrowser  
import random
import math
from bs4 import BeautifulSoup
import requests
import pywhatkit as pwk
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


Time = datetime.datetime.now().strftime("%H:%M:%S")
hours = datetime.datetime.now().strftime("%H")
minutes = datetime.datetime.now().strftime("%M")
seconds = datetime.datetime.now().strftime("%S")


def time():
    hour = int(hours)
    if hour >= 12:
        hourss = int(hours) - 12
        speak(f'It\'s {str(hourss)}:{str(minutes)} PM' ) 
    else:
        speak(f'It\'s {str(hours)}:{str(minutes)} AM' ) 

# Speech Recogniton variables
recorder = sr.Recognizer()
mic = sr.Microphone()
# Time variable
tday = datetime.date.today()
# Initializing speak function

def speak(audio):
    print(f'Pocket: '+audio)
    os.system(f'espeak -ven-us -p80 -s180 "{audio}"')

# Welcome the user

def wishMe():
    time = int(datetime.datetime.now().hour)
    if time >= 0 and time < 12:
        speak(f'Good Morning ,!')

    if time >= 12 and time < 18:
        speak(f'Good Afternoon ,!')

    if time >= 18 and time !=0:
        speak(f'Good Evening ,!')



def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f'')
        print("Listening...")
        r.pause_threshold = 1
        hearing = r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f'User: ' + query)
    except:
        query = "_"

        
    return query


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word)  for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words= clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda  x:x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list,intents_json):
    tag= intents_list[0]['intent']
    list_of_intents =intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

wishMe()
speak('Ready for anything.')
while True:
    command = myCommand().lower()
    ints = predict_class(command)
    res = get_response(ints, intents)
    if res == "Sorry, can't understand you":
        pass
    elif res == 'Goodbye' or res == 'bye':
        speak(res)
    elif ('start' or 'create') in command and ('project' or 'repo') in command:
        path = "/home/codemap/Documents/Projects/"
        while True:
            speak('What should I name it?')
            project_name = myCommand().lower()
            if project_name == "" or project_name =="_" :
                while True:
                    speak('Sorry, I did"nt catch that.')
                    project_name = myCommand().lower()
                    if project_name == "" or project_name == "_":
                        speak('Sorry, I did"nt catch that.')
                        project_name = myCommand().lower()
                        pass
                    else:
                        break
            else:
                break
        project_name = project_name.replace(' ','-')
        username = "MadhanDevlpr"
        webbrowser.open('https://github.com/new')
        ts.sleep(10)
        pg.click(x=930, y=495)
        pg.write(project_name)
        ts.sleep(5)
        pg.scroll(-1000)
        pg.click(x=690,y=905)
        ts.sleep(5)
        pg.hotkey('ctrl','alt','t')
        ts.sleep(3)
        pg.write(f'cd {path}')
        pg.press('enter')
        pg.write(f'git clone git@github.com:{username}/{project_name}.git')
        pg.press('enter')
        pg.hotkey('alt','f4')

        speak(f"Succesfully created repository {project_name}")
    elif ('what' in command and 'time' in command) or ('tell' in command and 'time' in command):
        time()
    elif 'how' in command.split()[0]:
        final = command.replace('how to','')
        webbrowser.open(f'https://google.com/search?q={final}')
        speak(f'Got some results regarding {final}.')
    elif 'what' in command.split()[0]:
        final = command.replace('what is','')
        webbrowser.open(f'https://google.com/search?q={final}')
        data = wikipedia.summary(final, sentences=2)
        data = data.replace('"','')
        try:
            speak(f'According to wikipedia, {data}.')
        except:
            speak(f'Got you some results regarding {final}')
    elif 'who is' in command:
        final = command.replace('who is','')
        webbrowser.open(f'https://google.com/search?q={final}')
        data = wikipedia.summary(final, sentences=2)
        try:
            speak(f'According to wikipedia, {data}.')
        except:
            speak(f'Got you some results about {final}')
    
    elif 'google' ==command:
        speak("The next time tell me what to search for., I've got no info from you to search")
    elif 'google' in command:
        final = command.replace('google','')
        webbrowser.open(f'https://google.com/search?q={final}')
        speak(f'Got some results regarding {final}.')
    elif 'multiply' in command or (('by' in command or 'with' in command ) and 'into' in command):
        try:
            res = [float(i) for i in command.split() if isfloat(i)]
            product = res[0] * res[1]
            speak(f"It's {product}.")
        except:
            speak('That was too tuff for me.')
    elif 'divide' in command and ('by' in command or 'with' in command):
        try:
            res = [float(i) for i in command.split() if isfloat(i)]
            final = res[0]/res[1]
            speak(f"It's {final}.")
        except:
            speak('That was too tuff for me.')
    elif 'subtract' in command or ('from' in command or '-' in command or 'minus' in command):
        try:
            res = [float(i) for i in command.split() if isfloat(i)]
            remainder = res[0] - res[1]
            speak(f"It's {remainder}.")
        except:
            speak('That was too tuff for me.')
    elif 'add' in command or ('with' in command or '+' in command or 'plus' in command):
        try:
            res = [float(i) for i in command.split() if isfloat(i)]
            sum = res[0] + res[1]
            speak(f"It's {sum}.")
        except:
            speak('That was too tuff for me.')
    elif ('what' in command or 'find' in command):
        if 'area' in command:
            if 'triangle' in command:
                if 'base' in command and 'height' in command:
                    res = [float(i) for i in command.split() if isfloat(i)]
                    try:
                        area = format((0.5*res[0]*res[1]),'.2f')
                        speak(f'Area of that triangle is {area} square units.')
                    except:
                        speak('Probably you wanna correct your question.')
                else:
                    res = [float(i) for i in command.split() if isfloat(i)]
                    try:
                        s = float(res[0] + res[1] + res[2]/2)
                        area = format((math.sqrt(s*(s-res[0])*(s-res[1])*(s-res[2]))),'.2f')
                        speak(f'Area of that triangle is {area} square units.')
                    except:
                        speak('Probably you wanna correct your question.')
            elif 'square' in command:
                res = [int(i) for i in command.split() if i.isdigit()]
                try:
                    area = res[0]**2
                    speak(f'Area of that triangle is {area} square units.')
                except:
                    speak('Probably you wanna correct your question.')
            elif 'rectangle' in command:
                try:
                    area = format(res[0] * res[1],'.2f')
                    speak(f'Area of that rectangle is {area} square units')
                except:
                    speak('Probably you wanna correct your question.')
        elif 'perimeter' in command:
            if 'triangle' in command:
                res = [float(i) for i in command.split() if isfloat(i)]
                try:
                    perimeter = format(res[0]+res[1]+res[2])
                    speak(f'Perimeter of that triangle is {perimeter} square units.')
                except:
                    speak('Probably you wanna correct your question.')
            elif 'square' in command:
                res = [int(i) for i in command.split() if i.isdigit()]
                try:
                    perimeter = 4*res[0]
                    speak(f'Perimeter of that triangle is {perimeter} square units.')
                except:
                    speak('Probably you wanna correct your question.')
            elif 'rectangle' in command:
                try:
                    area = format(res[0] * res[1],'.2f')
                    speak(f'Area of that rectangle is {area} square units')
                except:
                    speak('Probably you wanna correct your question.')
    elif ('play' in command and 'youtube' in command) or ('play' in command and 'music' in command) or ('start' in command and 'youtube' in command) or ('start' in command and 'music' in command):
        try:
            initial = command.replace('play ','')
            mid = command.replace('music','').replace('youtube','')
            final = command.replace('start','')
            pwk.playonyt(command)
            speak('There it is!')
        except:
            speak('Sorry, I had a problem playing it.')
    elif 'to sleep' in command:
        speak('I never sleep.')
    elif 'close' in command or 'close that' in command or 'close it' in command or 'close the' in command:
        if 'tab' in command:
            pg.hotkey('ctrl','w')
            speak('Tab closed.')
        else:
            pg.hotkey('alt','f4')
            speak('Window closed.')
    elif 'open' in command or 'start' in command:
        query = command.split()
        try:
            if 'terminal' in query:
                pg.hotkey('ctrl','alt','t')
                speak('Here you go!')
            elif 'sublime' in query:
                os.system('subl .')
                speak('Here you go!')
            else:
                search = command
                url = 'https://www.google.com/search'

                headers = {
                    'Accept' : '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
                }
                parameters = {'q': search}

                content = requests.get(url, headers = headers, params = parameters).text
                soup = BeautifulSoup(content, 'html.parser')

                search = soup.find(id = 'search')
                first_link = search.find('a')

                final_link = first_link['href']   
                webbrowser.open(final_link)
                speak('There it is!')
        except:
            speak('Probably, that is a unopenable object.')
    elif 'shutdown' in command or 'shut' in command and 'down' in command:
        closing = True
        speak(f'Do you really need to shutdown?')
        while closing:
            yesorno = myCommand()
            if 'yes' in yesorno.lower():
                speak('See you again.')
                os.system(f'shutdown now')
                sys.exit()
            else:
                speak(f"It's a right choice.!")
                closing = False
    


    elif 'search for' in command:
        query = command.split()

        initial_query = query[2:]

        final_query = ' '.join(initial_query)

        webbrowser.open(f'https://google.com/search?q={final_query}')
        try:
            data = wikipedia.summary(command, sentences=2)
            speak('According to wikipedia, '+data)
        except:
            speak('Got you some results from the web.')
    elif 'what' in command and 'weather' in command:
        webbrowser.open('https://www.google.com/search?&q=google+weather')
        speak('Have a nice day!')
    elif ('quit' or 'break') in command:
        speak('See you again!')
        sys.exit()
    elif 'what can you do' in command or 'your features' in command:
        speak("I simplify everything on your desktop.")
        speak('I also can open your favourite application and play videos in youtube.')
    else:
        if command == "bye" or command == "Goodbye":
            ints = predict_class(command)
            res = get_response(ints, intents)
            print("| Bot:", res)
            print("|===================== The Program End here! =====================|")
            exit()
        if command == "_":
            speak('I can\'t hear it properly, can you please say it again')
            continue
        else:
            ints = predict_class(command)
            res = get_response(ints, intents)
            try:
                if res == "Sorry, can't understand you":
                    pass
                else:
                    speak(res)
            except:
                webbrowser.open(f'https://google.com/search?q={command}')
                speak(f'Got you some results regarding that.')


                