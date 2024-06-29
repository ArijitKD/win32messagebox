# win32messagebox
A cross-platform Python package, compatible with tkinter's messagebox module, that provides an API for Windows-like messageboxes.

# Known issues (for non-Windows systems only):
* Messagebox may permanently lose focus, or gain focus only on hover, if grab is set on some other window by clicking.
* There may be times when the messagebox would be displayed without focus on any buttons, normally focus is set on the button specified by the ```-default``` option.
* Messagebox has system-wide modality, it always appears on top of every other active window. This behaviour cannot be changed.
