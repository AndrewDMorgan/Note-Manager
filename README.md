# Note-Manager
A basic task manager I'm working on in my free time. I'm trying to create a clean and expandable system that is highly functional. My goal is to create a fully functional task manager I can use in my daily life. I'm also wanting to improve my skills in making UI and create a nice, clean, understandable UI. I I may try to port it to android after completion but probably not.

## Much more information bellow

![Note Manager Screenshot (10/28/22)](https://github.com/AndrewDMorgan/Note-Manager/blob/main/Screen%20Shot%202022-11-01%20at%2010.51.47%20PM.png?raw=true)

## Current Features
 * Noteboard veiwing and selecting
 * Note viewing
 * Note and noteboard reordering
 * Dark mode theme
 * Dropdown menus on notes for sub notes
 * Resizeable window
 * Circles around buttons when hovering over them

## Planned Features
 * Calander/timed events
 * Catagories within note boards
 * Completing tasks
 * Adding notes and note boards
 * Settings to customize the application
 * Saving and auto saving
 * Add creation of sub-notes/descriptions
 * Sub notes rendering
 * Different sorting modes for calander events
 * Different views, calander view, note view, ect... with different ordering/sorting options
 * Light mode theme
 * So many other features I haven't though of hopefully

## Recently Updated
 * Replaced manual collition with pygame.Rect improving rendering of circle around hovered over buttons
 * Added basic typing field class, more functionality coming
 * Added Events.py to manage keyboard/mouse events
 * Refactored code to work but Events.py (cleaned up parameters A LOT)
 * Added a class to link a TextBoxContainer to a TypingBox

## Bugs
 * Theoretically all items to the side in a 2D grid of TextBoxContainer's will be shifted with the shift method
 * Fixed 10/31/22 - when reording items with dropped menus the spacing would be thrown off (the wrong id/index was used, the origonal one instead of the shifted one was used)
 * No problematic bugs so far, knock on wood
