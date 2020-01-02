import rumps
import os
import json
from subprocess import PIPE, Popen, STDOUT

rumps.debug_mode = True

CONFIG_FILE_NAME = "userConfig.json"

ADD_USER = "Add User"
SEPARATOR = "----"

def cmd_exec(cmd):
    os.system(cmd)

def change_username(username):
    cmd = 'git config --global user.name "{}"'.format(username)
    cmd_exec(cmd)

def change_user_email(email):
    cmd = 'git config --global user.email "{}"'.format(email)
    cmd_exec(cmd)
    
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
        self.menu.insert_before(ADD_USER, separator)
        
        self.read_user_config()
        selected_user_emails = self.get_current_user()
        
        self.build_user_menu()
            
    def build_user_menu(self):
        for user_config in self.user_data:
            self.add_new_user_to_menu(user_config)
    
    def read_user_config(self):
        try:
            with open(CONFIG_FILE_NAME) as config_file:
                self.user_data = json.load(config_file)
                for user_config in self.user_data:
                    self.all_emails.append(user_config['email'])
        except IOError:
            rumps.alert(CONFIG_FILE_NAME + " is not found in Resources folder. Make sure you have one there")
            
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
        
        is_selected = email in self.selected_emails

        new_menu_item = rumps.MenuItem(buttonName, self.create_user_btn_callback())
        new_menu_item.state = int(is_selected)

        return new_menu_item

    def add_new_user_to_menu(self, user_config):
        new_menu_item = self.create_menu_item(user_config)
        if not new_menu_item is None:
            self.menu.insert_before(SEPARATOR, new_menu_item)
            if new_menu_item.state:
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
        self.disable_all()
        window = rumps.Window('Enter button name, username and email.\nEach must be on a new line', 'Add User', "", "Next", True)
        response = window.run()
        if not response.clicked:
            return

        [buttonName, userName, email]  = response.text.split('\n')
        user_config = self.add_user_config(buttonName, userName, email)
        if user_config is None:
            return None

        new_menu_item = self.add_new_user_to_menu(user_config)
        self.menu.insert_before(SEPARATOR, new_menu_item)
        
    def create_user_btn_callback(self):
        that = self
        def callback(self):
            self.state = not self.state
            that.switch_users()
        return callback
    
    def switch_users(self):
        # TODO: change user config file format to return dic, instead of list
        usernames = []
        emails = []
        titles = []
        selected_item_titles = list(map(
            lambda menu_item: menu_item.title,
            filter(
                lambda menu_item: bool(menu_item.state),
                self.menu.values()
            )
        ))
        for user in self.user_data:
            if user['title'] in selected_item_titles:
                usernames.append(user['username'])
                emails.append(user['email'])
                titles.append(user['title'])
        change_username(', '.join(usernames))
        change_user_email(', '.join(emails))
        if len(usernames):
            self.set_title_username(', '.join(titles))
        else:
            self.set_title_username('none selected')
            

    def is_not_empty(self, string):
        return bool(string.strip())
    
    def set_title_username(self, username): 
        self.title = 'Git: ' + username

    def disable_all(self):
        for item in self.menu.values():
            item.state = 0

if __name__ == "__main__":
    GitAuthorSwitcher().run()