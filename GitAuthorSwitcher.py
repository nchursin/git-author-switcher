import rumps
import os
import json

rumps.debug_mode = True

CONFIG_FILE_NAME = "userConfig.json"

class GitAuthorSwitcher(rumps.App):
    def __init__(self):
        super(GitAuthorSwitcher, self).__init__("Git Author Switcher")
        self.menu = ["Add User"]
        try:
            with open(CONFIG_FILE_NAME) as config_file:
                self.config_data = json.load(config_file)
                for user_config in self.config_data:
                    self.add_new_user_to_menu(user_config)
        except IOError:
            print("File not accessible")
    
    def create_menu_item(self, user_config):
        if not self.is_user_config_valid(user_config):
            return None

        buttonName = user_config["title"]
        userName = user_config["username"]
        email = user_config["email"]

        userSelector = self.selectUserDec(userName, email)
        newMenuItem = rumps.MenuItem(buttonName, callback=userSelector)
        return newMenuItem

    def add_new_user_to_menu(self, user_config):
        new_menu_item = self.create_menu_item(user_config)
        if not new_menu_item is None:
            self.menu.insert_before("Add User", new_menu_item)

    def add_user_config(self, title, username, email):
        user_config = {
            'title': title,
            'username': username,
            'email': email,
        }
        if not self.is_user_config_valid(user_config):
            return None
        self.config_data.append(user_config)
        return user_config
    
    def is_user_config_valid(self, user_config):
        if user_config is None:
            return False
        buttonName = user_config["title"]
        userName = user_config["username"]
        email = user_config["email"]
        return self.is_not_empty(buttonName) and self.is_not_empty(userName) and self.is_not_empty(email)

    @rumps.clicked("Add User")
    def addUser(self, sender):
        self.disableAll()
        window = rumps.Window('Enter button name, username and email.\nEach must be on a new line', 'Add User', "", "Next", True)
        response = window.run()
        print(response)
        if not response.clicked:
            return

        [buttonName, userName, email]  = response.text.split('\n')
        user_config = self.add_user_config(buttonName, userName, email)
        if user_config is None:
            return None

        self.add_new_user_to_menu(user_config)


    def is_not_empty(self, string):
        return bool(string.strip())

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