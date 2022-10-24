import sys
import unreal
sys.path.append("F:/Projects/Repo/Python/Unreal/PythonScripts/venv/Lib/site-packages")

from PySide2 import QtCore, QtWidgets, QtGui, QtUiTools

editor_level_lib = unreal.EditorLevelLibrary()


class SimpleGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SimpleGUI, self).__init__(parent)

        # load the created ui widget
        self.widget = QtUiTools.QUiLoader().load("F:\\Projects\\Repo\\Python\\Unreal\\PythonScripts\\Qt\\basic.ui")

        # attach the widget to the "self" GUI
        self.widget.setParent(self)

        # set the UI geometry (if UI is not centered/visible)
        self.widget.setGeometry(0, 0, self.widget.width(), self.widget.height())

        # find the interaction elements
        self.text_l = self.widget.findChild(QtWidgets.QLineEdit, "textBox_L")
        self.text_r = self.widget.findChild(QtWidgets.QLineEdit, "textBox_R")
        self.checkbox = self.widget.findChild(QtWidgets.QCheckBox, "checkBox")

        self.slider = self.widget.findChild(QtWidgets.QSlider, "horizontalSlider")
        self.slider.sliderMoved.connect(self.on_slide)

        self.btn_ok = self.widget.findChild(QtWidgets.QPushButton, "okButton")
        self.btn_ok.clicked.connect(self.ok_clicked)

        self.btn_cancel = self.widget.findChild(QtWidgets.QPushButton, "cancelButton")
        self.btn_cancel.clicked.connect(self.cancel_clicked)

    # triggered on click of okButton
    def ok_clicked(self):
        text_l = self.text_l.text()
        text_r = self.text_r.text()
        is_checked = self.checkbox.isChecked()

        unreal.log("Text Left Value: {}".format(text_l))
        unreal.log("Text Right Value: {}".format(text_r))
        unreal.log("Checkbox: {}".format(is_checked))

    # triggered on click of cancelButton
    def cancel_clicked(self):
        unreal.log("Canceled")
        self.close()

    def on_slide(self):
        slider_value = self.slider.value()

        # move the selected actor according to the slider value
        selected_actors = editor_level_lib.get_selected_level_actors()

        if len(selected_actors) > 0:
            actor = selected_actors[0]

            # get old transform, change y axis value and write back
            new_transform = actor.get_actor_transform()
            new_transform.translation.y = slider_value

            actor.set_actor_transform(new_transform, True, True)

        unreal.log("Slider Value: {}".format(slider_value))


# only create an instance of the GUI when it's not already running
app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)


# start the GUI
main_window = SimpleGUI()
main_window.show()
