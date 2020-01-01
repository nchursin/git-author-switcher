import rumps
import os
import json
from subprocess import PIPE, Popen, STDOUT

rumps.debug_mode = True

CONFIG_FILE_NAME = "userConfig.json"

ADD_USER = "Add User"
SEPARATOR = "----"

class GitAuthorSwitcher(rumps.App):
    all_emails = []
    selected_emails = []
    user_data = []
    
    def __init__(self):
        super(GitAuthorSwitcher, self).__init__("Git Author Switcher")
        self.form_menu()
            
    def form_menu(self):
        self.menu = [ADD_USER]
        separator = rumps.MenuItem(SEPARATOR)
        separator.state = -1
        self.menu.insert_before(ADD_USER, separator)
        
        self.read_user_config()
        selected_user_emails = self.get_current_user()
        
        self.build_menu(selected_user_emails)
            
    def build_menu(self, selected_emails):
        for user_config in self.user_data:
            is_selected = user_config['email'] in selected_emails
            self.add_new_user_to_menu(user_config, is_selected)
    
    def read_user_config(self):
        try:
            with open(CONFIG_FILE_NAME) as config_file:
                self.user_data = json.load(config_file)
                for user_config in self.user_data:
                    self.all_emails.append(user_config['email'])
        except IOError:
            print("File not accessible")
            
    def get_current_user(self): 
        current_git_useremail = Popen(["git", "config", "--global", "user.email"], stdout=PIPE).communicate()[0].strip().decode("utf-8")
        user_emails = list(map(lambda text: text.strip(), current_git_useremail.split(',')))
        self.selected_emails = list(
            filter(
                lambda email: email in self.all_emails,
                user_emails
            )
        )
        return user_emails
    
    def create_menu_item(self, user_config):
        if not self.is_user_config_valid(user_config):
            return None

        buttonName = user_config["title"]
        userName = user_config["username"]
        email = user_config["email"]

        user_selector = self.select_user_dec(userName, email)
        newMenuItem = rumps.MenuItem(buttonName, callback=user_selector)
        return newMenuItem

    def add_new_user_to_menu(self, user_config, is_selected):
        new_menu_item = self.create_menu_item(user_config)
        if not new_menu_item is None:
            new_menu_item.state = int(is_selected)
            self.menu.insert_before(SEPARATOR, new_menu_item)
            if is_selected:
                self.set_title_username(user_config['title'])

    def add_user_config(self, title, username, email):
        user_config = {
            'title': title,
            'username': username,
            'email': email,
        }
        if not self.is_user_config_valid(user_config):
            return None
        self.user_data.append(user_config)
        with open(CONFIG_FILE_NAME, "w") as outfile:
            json.dump(self.user_data, outfile)
        return user_config
    
    def is_user_config_valid(self, user_config):
        if user_config is None:
            return False
        buttonName = user_config["title"]
        userName = user_config["username"]
        email = user_config["email"]
        return self.is_not_empty(buttonName) and self.is_not_empty(userName) and self.is_not_empty(email)

    @rumps.clicked(ADD_USER)
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
        self.menu.insert_before(SEPARATOR, new_menu_item)


    def is_not_empty(self, string):
        return bool(string.strip())
    
    def set_title_username(self, username): 
        self.title = 'Git: ' + username

    def select_user_dec(self, username, email):
        that = self
        def user_selector(self):
            that.set_title_username(username)
            userChangeCmd = 'git config --global user.name "{}"'.format(username)
            emailChangeCmd = 'git config --global user.email "{}"'.format(email)
            os.system(userChangeCmd)
            os.system(emailChangeCmd)
        return user_selector

    def disableAll(self):
        print(self.menu.values)
        for item in self.menu.values():
            item.state = 0

if __name__ == "__main__":
    GitAuthorSwitcher().run()