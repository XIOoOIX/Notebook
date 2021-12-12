#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout
import json
app = QApplication([])

notes = {"Добро пожаловать!" : {"текст" : "Это самое лучшее приложение для заметок в мире!", "теги" : ["добро","инструкция"]}}

with open("notes_data.json", "w") as file:
    json.dump(notes,file)

wnote = QWidget()
wnote.setWindowTitle('Умные заметки')
wnote.resize(900,600)

listnote = QListWidget()
listnotelab = QLabel('Список заметок')

buttonnotecreate = QPushButton('Создать заметку')
buttonnotedel = QPushButton('Удалить заметку')
buttonnotesave = QPushButton('Сохранить заметку')

fieldtag = QLineEdit('')
fieldtag.setPlaceholderText('Введите тег')
fieldtext = QTextEdit()
buttontagadd = QPushButton('Добавить к заметке')
buttontagdel = QPushButton('Открепить от заметки')
buttontagser = QPushButton('Искать заметки по тегу')
listtags = QListWidget()
listtagslab = QLabel('Список тегов')

layoutnotes = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(fieldtext)

col2 = QVBoxLayout()
col2.addWidget(listnotelab)
col2.addWidget(listnote)
row1 = QHBoxLayout()
row1.addWidget(buttonnotecreate)
row1.addWidget(buttonnotedel)
row2 =  QHBoxLayout()
row2.addWidget(buttonnotesave)
col2.addLayout(row1)
col2.addLayout(row2)

col2.addWidget(listtagslab)
col2.addWidget(listtags)
col2.addWidget(fieldtag)
row3 = QHBoxLayout()
row3.addWidget(buttontagadd)
row3.addWidget(buttontagdel)
row4 = QHBoxLayout()
row4.addWidget(buttontagser)

col2.addLayout(row3)
col2.addLayout(row4)

layoutnotes.addLayout(col1, stretch = 2)
layoutnotes.addLayout(col2, stretch = 1)
wnote.setLayout(layoutnotes)

def add_note():
    note_name, ok = QInputDialog.getText(wnote, "Добавьте заметку", "Название заметки: ")
    if ok and note_name != "":
        notes[note_name] = {"текст" : "", "теги" : []}
        listnote.addItem(note_name)
        listtags.addItems(notes[note_name]["теги"])
        print(notes)

def show_note():
    key = listnote.selectedItems()[0].text()
    print(key)
    fieldtext.setText(notes[key]["текст"])
    listtags.clear()
    listtags.addItems(notes[key]["теги"])

def save_note():
    if listnote.selectedItems():
        key = listnote.selectedItems()[0].text()
        notes[key]["текст"] = fieldtext.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Не выбрано')

def del_note():
    if listnote.selectedItems():
        key = listnote.selectedItems()[0].text()
        del notes[key]
        listnote.clear()
        listtags.clear()
        fieldtext.clear()
        listnote.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Не выбрано')

def add_tag():
    if listnote.selectedItems():
        key = listnote.selectedItems()[0].text()
        tag = fieldtag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            listtags.addItem(tag)
            fieldtag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Тег не выбран!')

def del_tag():
    if listtags.selectedItems():
        key = listnote.selectedItems()[0].text()
        tag = listtags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        listtags.clear()
        listtags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print('Тег не выбран!')

def search_tag():
    print(buttontagser.text())
    tag = fieldtag.text()
    if buttontagser.text() == "Искать заметки по тегу" and tag:
        print(tag)
        notesfilter = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notesfilter[note] = notes[note]
            buttontagser.setText('Сбросить поиск')
            listnote.clear()
            listtags.clear()
            listnote.addItems(notesfilter)
            print(buttontagser.text())
    elif buttontagser.text() == "Сбросить поиск":
        fieldtag.clear()
        listnote.clear()
        listtags.clear()
        listnote.addItems(notes)
        buttontagser.setText('Искать заметки по тегу')
        print(buttontagser.text())
    else:
        pass
buttonnotecreate.clicked.connect(add_note)
listnote.itemClicked.connect(show_note)
buttonnotesave.clicked.connect(save_note)
buttonnotedel.clicked.connect(del_note)
buttontagadd.clicked.connect(add_tag)
buttontagdel.clicked.connect(del_tag)
buttontagser.clicked.connect(search_tag)


wnote.show()

with open("notes_data.json", "r") as file:
    notes = json.load(file)
listnote.addItems(notes)

app.exec_()


