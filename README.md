# win32messagebox
A Python package for Linux and MacOS, compatible with tkinter's messagebox module, that provides a Windows-like message box.

# Known issues:
* Messagebox may permanently lose focus, or gain focus only on hover, if grab is set on some other window by clicking.
* There may be times when the messagebox would be displayed without focus on any buttons, normally focus is set on the button specified by the ```-default``` option.
* Messagebox has system-wide modality, it always appears on top of every other active window. This behaviour cannot be changed.
