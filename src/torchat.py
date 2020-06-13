
#### New commit, Tor working
##
#
# Needs to be rewrittten for Python 3.x
import config
#import wxversion
'''
Removed old code for some non-needed checks
'''
import wx
import os
import tc_client
import tc_gui

def main():
    #print "(2) wxPython version %s" % wx.version()
    #create the mandatory wx application object
    if config.isMac():
        import tc_mac
        app = tc_mac.App(redirect=False)
    else:
        app = wx.App(redirect=False)

    #test for availability of our listening port
    interface = config.get("client", "listen_interface")
    port = config.getint("client", "listen_port")
    print "(1) opening TorChat listener on %s:%s" % (interface, port)
    listen_socket = tc_client.tryBindPort(interface, port)
    if not listen_socket:
        print "(1) %s:%s is already in use" % (interface, port)
        wx.MessageBox(tc_gui.lang.D_WARN_USED_PORT_MESSAGE % (interface, port),
                      tc_gui.lang.D_WARN_USED_PORT_TITLE)
        return
    else:
        print "(1) TorChat is listening on %s:%s" % (interface, port)

    #now continue with normal program startup
    print "(1) start initializing main window"
    app.mw = tc_gui.MainWindow(listen_socket)
    app.SetTopWindow(app.mw)
    print "(1) main window initialized"
    print "(1) entering main loop"
    app.MainLoop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        tc_client.stopPortableTor()
