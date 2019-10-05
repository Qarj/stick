# stick
Backup files to a USB stick

Needs Python 3. Windows only.

```
pip install pypiwin32
```

Specify destination and folders to back up in a `stick.ini` file.

Destination folder must exist.

```
[DEFAULT]
dest = D:\stick

[source1]
source = C:\git\stick\test\source1

[source2]
source = C:\git\stick\test\source2

[source3]
source = C:\git\stick\test\does_not_exist
```

Create a shortcut to stick.py on your desktop and double click to update your backup.