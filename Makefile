all: ds build run

allt: ds test

build:
	pyinstaller --onefile -w main.py

run:
	dist/main.exe

test:
	python main.py

ds:
	python.exe -m PyQt6.uic.pyuic designer\mainwindow.ui -o package\ui\mainwindow_ui.py
	python.exe -m PyQt6.uic.pyuic designer\add_task_dialog.ui -o package\ui\add_task_dialog_ui.py
	python.exe -m PyQt6.uic.pyuic designer\remove_task_dialog.ui -o package\ui\remove_task_dialog_ui.py