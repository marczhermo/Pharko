# Pharko
A Sublime Text 3 plugin for organising shared snippets by you and other community members.

With the advent of React components with JSX syntax and Vue single-file-components, a single file can contain a section with javascript, css, and html in which multiple snippets scopes feature might fall short. The idea here is to organize them in a folder structure that suits your needs.

A typical example of folder organization is by having the file type/extension as the root folder, then sub-folder to your heart's content which will contain the actual snippet files. By following this simple folder structure, we open ourselves with a lot of possibilities which will help us expand our toolbelt just like any other Sublime power user.

* Existing javascript, css and html snippets will work with React or Vue compoments.
* There is no need to update the snippets file, just to add more scopes.
* The community can create a snippets reposity at Github (and others) to share their source codes to other users.
* Public repositories can be manually installed inside this package folder, and will be read by this package.
* You don't have to memorize each snippet's trigger keys, because directory traversal seems ways easier when you use the extension names or properly describe directory names.

## Quickpanel Shortcut
Add the following keyboard shortcut to your Key Bindings file

 `{ "keys": ["alt+shift+0"], "command": "pharko_list", "args": {} },`

## Todos
More improvements will come with this package since the author is just a starting to learn how to code in Python with Sublime package writing in mind.

* Create and read configuration settings
* Automatically install public snippets repository
