# Git Author Switch

This is a simple Mac menubar app to allow easy switch Git usernames.

Download a release from the [releases page](https://github.com/nchursin/git-author-switcher/releases).

Launch the app and click "Add User" in the app menu. This will open a window for you to enter user data:

* First line is for some label. This is how a user will be shown in the app menu
* Second line is the username
* Third line is for email

Please note that the app supports several users to be active for pair programming cases.

Currently there's no user deletion capability. To delete user you need to go to the `app/Resources` and remove user from `userConfig.json` file