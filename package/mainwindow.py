from PyQt6.QtWidgets import QMainWindow, QDialog, QTableWidgetItem
from package import connection_db
from package.ui.mainwindow_ui import Ui_MainWindow
from package.ui import add_task_dialog_ui
from package.ui import remove_task_dialog_ui
from package.ui import see_all_tasks_dialog_ui
from package.ui import edit_task_dialog_ui
from package.task import Task


class MainWindow(QMainWindow):
    connection, con_cursor = connection_db.get_connection()
    tasks = []
    no_deadline_exception = "NoDeadlineException: there's a column with no deadline"
    

    def __init__(self):
        super(MainWindow, self).__init__()

        self.con_cursor.execute("SELECT * FROM sqlite_master")

        if not bool(self.con_cursor.fetchall()): #check if db exists
            self.con_cursor.execute('''CREATE TABLE Items (
                                    title TEXT NOT NULL UNIQUE,
                                    description text,
                                    deadline datetime
                                    );''')
            
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_list()
        self.ui.listWidget.itemClicked.connect(self.task_done)
        self.ui.add_button.clicked.connect(self.add_it)
        self.ui.remove_button.clicked.connect(self.remove_it)
        self.ui.edit_button.clicked.connect(self.edit_it)
        self.ui.see_all_button.clicked.connect(self.see_it)
        self.ui.done_button.clicked.connect(self.task_done)
        self.show()


    def load_list(self):
        self.con_cursor.execute("SELECT * from Items")

        records = self.con_cursor.fetchall()

        for row in records:
            print(f"records: {records}")
            task = Task(row[0], row[2], row[1])

            if not self.is_already_on_list(task):
                self.tasks.append(task)
            self.today_list_widget()


    def is_already_on_list(self, task):
        for i in self.tasks:
            if i.title == task.title:
                return True
            
        return False


    def today_list_widget(self):
        try:
            if self.tasks[len(self.tasks) - 1].is_today():
                self.ui.listWidget.addItem(self.tasks[len(self.tasks) - 1].title)
                
        except:
            print(self.no_deadline_exception)


    def not_due_list_widget(self):
        try:
            if not self.tasks[len(self.tasks) - 1].is_due():
                pass
                #to implement

        except:
            print(self.no_deadline_exception)


    def was_clicked(self):
        self.go = True


    def add_it(self):
        self.go = False
        
        dialog = QDialog()
        ui = add_task_dialog_ui.Ui_Dialog()
        ui.setupUi(dialog)

        ui.buttonBox.accepted.connect(self.was_clicked)

        dialog.exec()

        if self.go:
            title = ui.task_title.toPlainText()
            deadline = ui.task_date.toPlainText()
            description = ui.task_details.toPlainText()

            self.tasks.append(Task(deadline, title, description))

            title = self.tasks[len(self.tasks) - 1].title
            deadline = self.tasks[len(self.tasks) - 1].deadline
            description = self.tasks[len(self.tasks) - 1].description

            self.con_cursor.execute("INSERT INTO Items VALUES (?, ?, ?)", (deadline, description, title))

            self.load_list()


    def remove_it(self):
        dialog = QDialog()
        ui = remove_task_dialog_ui.Ui_Dialog()
        ui.setupUi(dialog)

        dialog.exec()


    def see_it(self):
        dialog = QDialog()
        ui = see_all_tasks_dialog_ui.Ui_Dialog()
        ui.setupUi(dialog)

        self.con_cursor.execute("SELECT * from Items")

        records = self.con_cursor.fetchall()

        ui.tableWidget.setRowCount(3)
        ui.tableWidget.setColumnWidth(0, 260)
        ui.tableWidget.setColumnWidth(2, 542)

        r=0
        for row in records:
            ui.tableWidget.setItem(r, 0, QTableWidgetItem(row[0]))
            ui.tableWidget.setItem(r, 1, QTableWidgetItem(row[2]))
            ui.tableWidget.setItem(r, 2, QTableWidgetItem(row[1]))
            r+=1

        #ui.buttonBox.accepted.connect() ;;to implement
        #ui.buttonBox.rejected.connect() ;;to implement

        dialog.exec()


    def edit_it(self):
        dialog = QDialog()
        ui = edit_task_dialog_ui.Ui_Dialog()
        ui.setupUi(dialog)
        
        for i in self.tasks:
            ui.task_list.addItem(i.title)

        dialog.exec()

    
    def remove_task(self):
        try:
            title = self.ui.listWidget.currentItem().text()
            self.con_cursor.execute("DELETE FROM Items WHERE title=?", (title,))
        
            for i in self.tasks:
                if i.title.__eq__(title):
                    self.tasks.remove(i)
                    break

            print(self.tasks)

        except:
            print("nothing was selected")

        self.ui.listWidget.clear()
        self.load_list()


    def task_done(self):       
        self.ui.done_button.clicked.connect(self.remove_task)