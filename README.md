# homeServerAPI
### Depencencies:
- [bottle v0.12.25](https://pypi.org/project/bottle/0.12.25/)
- [Requests v2.31.0](https://pypi.org/project/requests/2.31.0/)

## Functionalities
### To do list
Currently used by my [browser-homepage](https://github.com/ale3d62/browser-homepage). 

Allows the use of a to do list where items can be `read`, `added`, `edited`, and `deleted` from any device that can connect to the server.

### Wallpapers
Currently used by my [browser-homepage](https://github.com/ale3d62/browser-homepage).

Allows the use of any collection of wallpapers from [Wallhaven](https://wallhaven.cc/), which allows for automatic wallpaper syncing when used along with my [Wallhaven auto downloader script](https://github.com/ale3d62/wallhaven-auto-downloader).

### Send youtube video to device (WIP)
Send the youtube video you are currently watching to another device so that you can continue watching from there.

**Important requirements**
- Devices need to be added to the ``receiverDevices.json`. Static IP assignment is needed for this. Furthermore, devices using windows need to have the following inbound firewall rule enabled in order to be pinged: `File and Printer Sharing (Echo Request - ICMPv4-In)`
- Windows receiver devices need to run my [Windows server receiver](https://github.com/ale3d62/windowsServerReceiver) script, other devices are not supported yet.
