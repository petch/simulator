from PyQt4.QtGui import *
from PyQt4.QtCore import *
from enum import Enum
from distutils.dir_util import *
import sys
import os

class Editor(Enum):
    projects    = 0
    domain      = 1
    problem     = 2
    runs        = 3
    results     = 4
    preferences = 5

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.settings = QSettings('MMR', 'Simulator')

        box = QHBoxLayout()
        main = QWidget()
        main.setLayout(box)
        self.setCentralWidget(main)

        box.addWidget(self.navigation())

        self.splitter = QSplitter(Qt.Horizontal)
        box.addWidget(self.splitter)

        self.editor = Editor.projects
        self.load(self.editor, False)

        self.restoreGeometry(self.settings.value('geometry', ''))
        self.restoreState(self.settings.value('state', ''))
        self.splitter.restoreState(self.settings.value('splitter' + self.editor.name, ''))
        self.setWindowTitle('Projects - Simulator')
        self.show()

    def closeEvent(self, event):
        self.settings.setValue('splitter' + self.editor.name, self.splitter.saveState())
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('state', self.saveState())
        QMainWindow.closeEvent(self, event)

    def navButton(self, editor):
        button = QToolButton()
        button.isCheckable = True
        button.setText(editor.name.title())
        button.clicked.connect(lambda state: self.load(editor))
        return button

    def navigation(self):
        box = QVBoxLayout()
        nav = QWidget()
        nav.setLayout(box)

        box.addWidget(self.navButton(Editor.projects))
        box.addWidget(self.navButton(Editor.domain))
        box.addWidget(self.navButton(Editor.problem))
        box.addWidget(self.navButton(Editor.runs))
        box.addWidget(self.navButton(Editor.results))
        box.addStretch(1)
        box.addWidget(self.navButton(Editor.preferences))

        return nav

    def load(self, editor, save_state=True):
        if save_state:
            self.settings.setValue('splitter' + self.editor.name, self.splitter.saveState())
        self.editor = editor

        if hasattr(self, 'side'):
            self.side.setParent(None)
        self.side = getattr(self, editor.name + 'Side')()
        if hasattr(self, 'work'):
            self.work.setParent(None)
        self.work = getattr(self, editor.name + 'Work')()

        self.splitter.addWidget(self.side)
        self.splitter.addWidget(self.work)
        self.splitter.restoreState(self.settings.value('splitter' + editor.name, ''))

    def addItem(self, tree, name):
        item = QTreeWidgetItem([name])
        item.name = name
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        tree.addTopLevelItem(item)
        return item

    def actionButton(self, tree, name, action, enableOnSelect=True):
        button = QToolButton()
        button.setText(name)
        button.clicked.connect(lambda state: action(tree))
        if enableOnSelect:
            button.setEnabled(tree.currentItem() is not None)
            tree.itemSelectionChanged.connect(lambda : button.setEnabled(tree.currentItem() is not None))
        return button

    def projectsSelected(self, tree):
        name = tree.currentItem().text(0)
        self.setWindowTitle(f'{name} - Projects - Simulator')
        pass

    def projectsNew(self, tree):
        while True:
            template = QFileDialog.getExistingDirectory(self, "Choose a project template", "problems", QFileDialog.ShowDirsOnly)
            if template == '':
                return
            if not os.path.exists(f'{template}/problem.py'):
                QMessageBox.information(self, f'Not project', f'Folder {template} is not project', QMessageBox.Ok)
            else:
                break
        name = os.path.basename(template)
        while os.path.exists(f'projects/{name}'):
            name = 'new ' + name
        copy_tree(template, f'projects/{name}')
        tree.setCurrentItem(self.addItem(tree, name))

    def projectClone(self, tree):
        name = source = tree.currentItem().text(0)
        while os.path.exists(f'projects/{name}'):
            name = 'clone ' + name
        copy_tree(f'projects/{source}', f'projects/{name}')
        tree.setCurrentItem(self.addItem(tree, name))

    def projectsDelete(self, tree):
        name = tree.currentItem().text(0)
        reply = QMessageBox.question(self, f'Delete {name}', f'Do you sure want to delete the project {name}?', QMessageBox.No, QMessageBox.Yes)
        if reply != QMessageBox.Yes:
            return
        remove_tree(f'projects/{name}')
        self.load(Editor.projects)

    def projectsMove(self, item):
        name = item.text(0)
        if name == item.name:
            return
        if os.path.exists(f'projects/{name}'):
            QMessageBox.information(self, f'Project exists', f'Projects with name {name} already exists', QMessageBox.Ok)
            item.setText(0, item.name)
            return
        os.rename(f'projects/{item.name}', f'projects/{name}')
        item.name = name

    def projectsSide(self):
        box = QVBoxLayout()
        side = QWidget()
        side.setLayout(box)

        tree = QTreeWidget()
        tree.setHeaderHidden(True)
        tree.itemSelectionChanged.connect(lambda : self.projectsSelected(tree))
        tree.itemChanged.connect(lambda item, column: self.projectsMove(item))
        root, projects, files = next(os.walk('projects'))
        for project in sorted(projects):
            self.addItem(tree, project)

        menuBox = QHBoxLayout()
        menuBox.addWidget(QLabel('Projects'), 1)
        menuBox.addWidget(self.actionButton(tree, 'New', self.projectsNew, False))
        menuBox.addWidget(self.actionButton(tree, 'Clone', self.projectClone))
        menuBox.addWidget(self.actionButton(tree, 'Delete', self.projectsDelete))
        menu = QWidget()
        menu.setLayout(menuBox)

        box.addWidget(menu)
        box.addWidget(tree)

        return side

    def projectsWork(self):
        area = QWidget()
        vBox = QVBoxLayout()

        menu = QWidget()
        vBox.addWidget(menu)
        menuBox = QHBoxLayout()
        menu.setLayout(menuBox)
        menuBox.addWidget(QLabel('Project1'), 1)
        menuBox.addWidget(QPushButton('Run'))
        menuBox.addWidget(QPushButton('Test'))

        view = QFrame()
        view.setFrameShape(QFrame.StyledPanel)
        vBox.addWidget(view, 1)

        area.setLayout(vBox)
        return area

    def domainSide(self):
        box = QVBoxLayout()
        side = QWidget()
        side.setLayout(box)

        menuBox = QHBoxLayout()
        menuBox.addWidget(QLabel('Shapes'), 1)
        menuBox.addWidget(QPushButton('New'))
        menuBox.addWidget(QPushButton('Clone'))
        menuBox.addWidget(QPushButton('Delete'))
        menu = QWidget()
        menu.setLayout(menuBox)
        box.addWidget(menu)

        tree = QTreeWidget()
        tree.setHeaderHidden(True)
        item = QTreeWidgetItem(['test'])
        tree.addTopLevelItem(item)
        box.addWidget(tree)

        return side

    def domainWork(self):
        area = QWidget()
        vBox = QVBoxLayout()

        menu = QWidget()
        vBox.addWidget(menu)
        menuBox = QHBoxLayout()
        menu.setLayout(menuBox)
        menuBox.addWidget(QLabel('Project1'), 1)

        view = QFrame()
        view.setFrameShape(QFrame.StyledPanel)
        vBox.addWidget(view, 1)

        area.setLayout(vBox)
        return area

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()