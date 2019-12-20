import rumps
import os

class GitAuthorSwitcher(rumps.App):
    def __init__(self):
        super(GitAuthorSwitcher, self).__init__("Git Author Switcher")
        self.menu = ["Nikita Aquiva", "Nikita Chursin", "Dmitriy Prozorovskiy"]


    @rumps.clicked("Nikita Aquiva")
    def selectNikitaAquiva(self, sender):
        self.disableAll()
        sender.state = 1
        self.selectUser('Nikita Chursin', 'fake@fake.fake')

    @rumps.clicked("Nikita Chursin")
    def selectNikita(self, sender):
        self.disableAll()
        sender.state = 1
        self.selectUser('Nikita Chursin', 'fake@fake.fake')

    @rumps.clicked("Dmitriy Prozorovskiy")
    def selectDima(self, sender):
        self.disableAll()
        sender.state = 1
        self.selectUser('Dmitriy Prozorovskiy', 'fake@fake.fake')

    def selectUser(self, username, email):
        self.title = 'Git: ' + username
        userChangeCmd = 'git config --global user.name "{}"'.format(username)
        emailChangeCmd = 'git config --global user.email "{}"'.format(email)
        os.system(userChangeCmd)
        os.system(emailChangeCmd)

    def disableAll(self):
        print(self.menu.values)
        for item in self.menu.values():
            print(item)
            item.state = 0

if __name__ == "__main__":
    GitAuthorSwitcher().run()