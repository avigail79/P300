import PySimpleGUI as sg


layout = [[sg.Text("Hello Subject!\n To start the experiment enter the parameters below:")], [sg.Button("OK")]]

# Create the window
window = sg.Window(title="Recording GUI", layout=layout, margins=(200, 100)).read()

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
