import PySimpleGUI as sg


def mainWin():
     # Define the layout of the window
    layout = [
        [sg.Text("Hello, PySimpleGUI!")],
        [sg.Button("Click me")],
        [sg.Multiline(default_text="This is a multiline element.", size=(15, 15), key="1")],
        [sg.Multiline(default_text="This is a multiline element.", size=(15, 15), key="2")],
        [sg.Multiline(default_text="This is a multiline element.", size=(15, 15), key="3")],
        [sg.Multiline(default_text="This is a multiline element.", size=(15, 15), key="4")],
        [sg.Multiline(default_text="This is a multiline element.", size=(15, 15), key="5")],
    ]

    # Create the window
    window = sg.Window("My PySimpleGUI Window", layout,size=(500,500))

    while True:
        # Read events and values from the window
        event, values = window.read()

        # Handle events
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Click me":
            sg.popup("Button clicked!")

    # Close the window
    window.close()
if __name__ == "__main__":
    mainWin()