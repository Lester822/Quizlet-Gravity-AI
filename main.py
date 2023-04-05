import pyautogui
import pytesseract
import time
import csv

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# Creates a CSV file. Not actually called in program, only for dev.
def makeCsv(name):
  file = open(name, 'w')  # Opens the Books csv
  write = csv.writer(file)
  write.writerow()


# Takes in dir and outputs list of rows from csv
def getCsvData(dir):
  file = open(dir, 'r')  # Opens the file in read mode
  read = csv.reader(file)
  data = []  # Creates enmpty list to put data in
  for row in read:
    data.append(row)  # Goes row by row adding them to a list
  return data


# Function can be called to ask user in console to add new row to given csv.
def manualInsert(direct):
  file = open(direct, 'a') # Opens the csv at the dir
  write = csv.writer(file)
  term = '0'
  while term.lower() != '-1':
    term = input('What is the first term? Or type -1 to exit.')
    if term == '-1':
      break
    definition = input('What is the definition?')
    write.writerow([term, definition])


# Takes in raw string from img -> txt, and formats w/out spaces, non-letters, and linebreaks.
def formatData(text):
    output = ''
    for character in text:
        if character.isalpha() and character != ' ' and character != '\n':
            output = output + character.lower()
    return output


def checkTerms(string, data):
  time.sleep(10)
  for row in data:
    if row[1] in string:
      pyautogui.write(row[0])
      pyautogui.press('enter')


def getText(img):
    return (pytesseract.image_to_string(img))

def answerWithTerm():
    termsAndDefs = getCsvData("terms.csv")
    for row in termsAndDefs:
        row[1] = formatData(row[1])
    while True:
        im2 = pyautogui.screenshot(region=(150,185, 1920, 650))
        screenText = formatData(getText(im2))
        for row in termsAndDefs:
            definition = row[1]
            #print(f'{definition} - {screenText}')  # This is just for monitoring what the text reader is seeing
            if definition[1:-1] in screenText: #or definition[7:18] in screenText:
                pyautogui.write(row[0])
                if screenText[0:6] == 'prompt':
                    time.sleep(2)
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('a')
                    pyautogui.press('backspace')
                    pyautogui.keyUp('ctrl')
                pyautogui.press('enter')
        if screenText == "playagain":
            break

answerWithTerm()