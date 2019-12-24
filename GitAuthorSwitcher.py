import rumps
import os

rumps.debug_mode = True

class GitAuthorSwitcher(rumps.App):
    def __init__(self):
        super(GitAuthorSwitcher, self).__init__("Git Author Switcher")
        self.menu = ["Nikita Personal", "Nikita Aquiva", "Nikita Selas", "Dmitriy Prozorovskiy"]

    @rumps.clicked("Nikita Personal")
    def selectNikitaPersonal(self, sender):
        self.disableAll()
        sender.state = 1
        self.selectUser('Nikita Chursin', 'chursinn91@gmail.com')

    @rumps.clicked("Nikita Aquiva")
    def selectNikitaAquiva(self, sender):
        self.disableAll()
        sender.state = 1
        self.selectUser('Nikita Chursin', 'fake@fake.fake')

    @rumps.clicked("Nikita Selas")
    def selectNikita(self, sender):
        self.disableAll()
        sender.state = 1
        self.selectUser('Nikita Chursin', 'fake@fake.fake')

    @rumps.clicked("Dmitriy Prozorovskiy")
    def selectDima(self, sender):
        self.disableAll()
        sender.state = 1
        self.selectUser('Dmitriy Prozorovskiy', 'fake@fake.fake')

    @rumps.clicked("Add User")
    def addUser(self, sender):
        self.disableAll()
        window = rumps.Window('Enter button name, username and email.\nEach must be on a new line', 'Add User', "", "Next", True)
        response = window.run()
        print(response)
        if not response.clicked:
            return

        [buttonName, userName, email]  = response.text.split('\n')
        if not (self.is_not_empty(buttonName) and self.is_not_empty(userName) and self.is_not_empty(email)):
            return

        userSelector = self.selectUserDec(userName, email)
        newMenuItem = rumps.MenuItem(buttonName, callback=userSelector)
        self.menu.insert_before("Add User", newMenuItem)


    def is_not_empty(self, string):
        return bool(string.strip())

    def selectUser(self, username, email):
        self.title = 'Git: ' + username
        userChangeCmd = 'git config --global user.name "{}"'.format(username)
        emailChangeCmd = 'git config --global user.email "{}"'.format(email)
        os.system(userChangeCmd)
        os.system(emailChangeCmd)

    def selectUserDec(self, username, email):
        that = self
        def userSelector(self):
            that.title = 'Git: ' + username
            userChangeCmd = 'git config --global user.name "{}"'.format(username)
            emailChangeCmd = 'git config --global user.email "{}"'.format(email)
            os.system(userChangeCmd)
            os.system(emailChangeCmd)
        return userSelector

    def disableAll(self):
        print(self.menu.values)
        for item in self.menu.values():
            item.state = 0

if __name__ == "__main__":
    GitAuthorSwitcher().run()