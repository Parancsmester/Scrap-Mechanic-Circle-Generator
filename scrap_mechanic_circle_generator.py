from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QColorDialog, QRadioButton, QLabel, QSpinBox, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PIL import Image, ImageDraw
from uuid import uuid4
from os import listdir, environ, makedirs

block_data = {
    'Concrete Block 1':'a6c6ce30-dd47-4587-b475-085d55c6a3b4',
    'Wood Block 1':'df953d9c-234f-4ac2-af5e-f0490b223e71',
    'Metal Block 1':'8aedf6c2-94e1-4506-89d4-a0227c552f1e',
    'Barrier Block':'09ca2713-28ee-4119-9622-e85490034758',
    'Tile Block':'8ca49bff-eeef-4b43-abd0-b527a567f1b7',
    'Brick Block':'0603b36e-0bdb-4828-b90c-ff19abcdfe34',
    'Glass Block':'5f41af56-df4c-4837-9b3c-10781335757f',
    'Glass Tile Block':'749f69e0-56c9-488c-adf6-66c58531818f',
    'Path Light Block':'073f92af-f37e-4aff-96b3-d66284d5081c',
    'Spaceship Block':'027bd4ec-b16d-47d2-8756-e18dc2af3eb6',
    'Cardboard Block':'f0cba95b-2dc4-4492-8fd9-36546a4cb5aa',
    'Scrap Wood Block':'1fc74a28-addb-451a-878d-c3c605d63811',
    'Wood Block 2':'1897ee42-0291-43e4-9645-8c5a5d310398',
    'Wood Block 3':'061b5d4b-0a6a-4212-b0ae-9e9681f1cbfb',
    'Scrap Metal Block':'1f7ac0bb-ad45-4246-9817-59bdf7f7ab39',
    'Metal Block 2':'1016cafc-9f6b-40c9-8713-9019d399783f',
    'Metal Block 3':'c0dfdea5-a39d-433a-b94a-299345a5df46',
    'Scrap Stone Block':'30a2288b-e88e-4a92-a916-1edbfc2b2dac',
    'Concrete Block 2':'ff234e42-5da4-43cc-8893-940547c97882',
    'Concrete Block 3':'e281599c-2343-4c86-886e-b2c1444e8810',
    'Cracked Concrete Block':'f5ceb7e3-5576-41d2-82d2-29860cf6e20e',
    'Concrete Slab Block':'cd0eff89-b693-40ee-bd4c-3500b23df44e',
    'Rusted Metal Block':'220b201e-aa40-4995-96c8-e6007af160de',
    'Extruded Metal Block':'25a5ffe7-11b1-4d3e-8d7a-48129cbaf05e',
    'Bubble Plastic Block':'f406bf6e-9fd5-4aa0-97c1-0b3c2118198e',
    'Plastic Block':'628b2d61-5ceb-43e9-8334-a4135566df7a',
    'Insulation Block':'9be6047c-3d44-44db-b4b9-9bcf8a9aab20',
    'Plaster block':'b145d9ae-4966-4af6-9497-8fca33f9aee3',
    'Carpet Block':'febce8a6-6c05-4e5d-803b-dfa930286944',
    'Painted Wall Block':'e981c337-1c8a-449c-8602-1dd990cbba3a',
    'Net Block':'4aa2a6f0-65a4-42e3-bf96-7dec62570e0b',
    'Solid Net Block':'3d0b7a6e-5b40-474c-bbaf-efaa54890e6a',
    'Punched Steel Block':'ea6864db-bb4f-4a89-b9ec-977849b6713a',
    'Striped Net Block':'a479066d-4b03-46b5-8437-e99fec3f43ee',
    'Square Mesh Block':'b4fa180c-2111-4339-b6fd-aed900b57093',
    'Restroom Block':'920b40c8-6dfc-42e7-84e1-d7e7e73128f6',
    'Diamond Plate Block':'f7d4bfed-1093-49b9-be32-394c872a1ef4',
    'Aluminium Block':'3e3242e4-1791-4f70-8d1d-0ae9ba3ee94c',
    'Worn Metal Block':'d740a27d-cc0f-4866-9e07-6a5c516ad719',
    'Spaceship Floor Block':'4ad97d49-c8a5-47f3-ace3-d56ba3affe50',
    'Sand Block':'c56700d9-bbe5-4b17-95ed-cef05bd8be1b',
    'Armored Glass Block':'b5ee5539-75a2-4fef-873b-ef7c9398b3f5'
}
color = None
radio_fill_isChecked = True
p = f'{environ["APPDATA"]}/Axolot Games/Scrap Mechanic/User/'
blueprint_path = f'{p}{listdir(p)[0]}/Blueprints/'

app = QApplication([])
app.setApplicationName('Scrap Mechanic Körgenerátor')
w = QWidget(styleSheet='QWidget {font-family: Arial; background-color: #71797e;} QMessageBox QLabel {color: white; font-weight: bold;}', windowIcon=QIcon('icon.png'), minimumWidth=500, maximumWidth=500)
cw = QWidget(styleSheet='QColorDialog QPushButton {font-family: Arial; color: black} QColorDialog {background: #1f2120} QColorDialog QLabel {font-family: Arial; color: white;}', windowIcon=QIcon('icon.png'))
label_for_block_list = QLabel(w, text='Blokk:', styleSheet='font-size: 25px; font-weight: bold; color: white;')
block_list = QComboBox(w, styleSheet='font-size: 25px; font-weight: bold; background: #d3d3d3')
colorchooser = QPushButton('Szín kiválasztása', w, styleSheet='font-size: 25px; font-weight: bold; background: #d3d3d3')
radio_fill = QRadioButton(w, text='Kitöltés', styleSheet='font-size: 20px; font-weight: bold; color: white;', checked=True)
radio_outline = QRadioButton(w, text='Körvonal    Vastagság:', styleSheet='font-size: 20px; font-weight: bold; color: white;')
spinbox_width = QSpinBox(w, styleSheet='font-size: 25px; font-weight: bold; background: #d3d3d3', maximum=1000, minimum=1, enabled=False, value=2)
label_warning = QLabel(w, text='Vigyázz! 1-es vastagság esetén lehetnek olyan blokkok, amelyek\nátlósan érintkeznek a többi blokkal, emiatt a kör széteshet!', styleSheet='font-size: 15px; font-weight: bold; color: red;', height=35)
label_warning.setHidden(True)
label_for_spinbox_size = QLabel(w, text='Méret:', styleSheet='font-size: 25px; font-weight: bold; color: white;')
spinbox_size = QSpinBox(w, styleSheet='font-size: 25px; font-weight: bold; background: #d3d3d3', maximum=1000, minimum=2)
generate = QPushButton('Generálás!', w, styleSheet='font-size: 25px; font-weight: bold; background: DarkGreen; color: white;')

layout_width = QHBoxLayout()
layout_width.addWidget(radio_outline)
layout_width.addWidget(spinbox_width)
layout_size = QHBoxLayout()
layout_size.addWidget(label_for_spinbox_size)
layout_size.addWidget(spinbox_size)
layout_block = QHBoxLayout()
layout_block.addWidget(label_for_block_list)
layout_block.addWidget(block_list)
layout = QVBoxLayout(w)
layout.addLayout(layout_block)
layout.addWidget(colorchooser)
layout.addWidget(radio_fill)
layout.addLayout(layout_width)
layout.addWidget(label_warning)
layout.addLayout(layout_size)
layout.addWidget(generate)

for i in block_data:
    block_list.addItem(i)
def fill_selected():
    global radio_fill_isChecked
    radio_fill_isChecked = True
    spinbox_width.setEnabled(False)
    spinbox_width.setValue(2)
def outline_selected():
    global radio_fill_isChecked
    radio_fill_isChecked = False
    spinbox_width.setEnabled(True)
def spinbox_width_changed():
    if spinbox_width.value() == 1:
        label_warning.setHidden(False)
    else:
        label_warning.setHidden(True)
def ch():
    global color
    colordialog = QColorDialog(parent=cw)
    color = colordialog.getColor(parent=cw).name().strip('#')
    colorchooser.setStyleSheet(f'font-size: 25px; font-weight: bold; background: #{color}')
def gen():
    if color is None:
        QMessageBox(QMessageBox.Critical, 'Hiba', 'Nem adtál meg színt!', QMessageBox.Ok, w).exec_()
    else:
        im = Image.new('RGBA', (spinbox_size.value(), spinbox_size.value()))
        draw = ImageDraw.Draw(im)
        if radio_fill_isChecked:
            draw.ellipse((0, 0, spinbox_size.value()-1, spinbox_size.value()-1), fill='#'+color)
        else:
            draw.ellipse((0, 0, spinbox_size.value()-1, spinbox_size.value()-1), outline='#'+color, width=spinbox_width.value())
        pixels = im.load()
        wrap = []
        childs = []
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                wrap.append((x,y,pixels[x,y]))
        for x, y, c in wrap:
            if c != (0, 0, 0, 0):
                childs.append(f'{{"bounds":{{"x":1,"y":1,"z":1}},"color":"{color.lower()}","pos":{{"x":{-x},"y":{y},"z":0}},"shapeId":"{block_data[block_list.currentText()]}","xaxis":1,"zaxis":3}}')
        ch = ','.join([child for child in childs])
        im.resize((128, 128))
        while True:
            _uuid = str(uuid4())
            try:
                makedirs(f'{blueprint_path}{_uuid}')
            except FileExistsError:
                continue
            else:
                break
        try:
            with open(f'{blueprint_path}{_uuid}/blueprint.json', 'w') as f:
                f.write(f'{{"bodies":[{{"childs":[{ch}]}}],"version":3}}')
            with open(f'{blueprint_path}{_uuid}/description.json', 'w') as f:
                f.write(f'{{"description":"Generált kör\nMéret: {spinbox_size.value()}\nSzín: {color.lower()}\nBlokk: {block_list.currentText()}\nBlokk shapeID: {block_data[block_list.currentText()]}","localId":"{_uuid}","name":"#{color.lower()} Kör {spinbox_size.value()} {block_list.currentText()}","type":"Blueprint","version":0}}')
            im.save(f'{blueprint_path}{_uuid}/icon.png')
        except:
            QMessageBox(QMessageBox.Critical, 'Hiba', 'Mentés sikertelen!', QMessageBox.Ok, w).exec_()
            pass
        else:
            QMessageBox(QMessageBox.Information, 'Információ', 'Generálás és mentés sikeres!', QMessageBox.Ok, w).exec_()
        
colorchooser.clicked.connect(ch)
radio_fill.toggled.connect(fill_selected)
radio_outline.toggled.connect(outline_selected)
spinbox_width.valueChanged.connect(spinbox_width_changed)
generate.clicked.connect(gen)
w.show()
app.exec_()
