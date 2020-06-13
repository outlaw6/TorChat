
#### New commit, Tor working
##
#
# Needs to be rewrittten for Python 3.x
import config
#import wxversion
'''
if config.isMac():
    if wxversion.checkInstalled('2.9'):
        wxversion.select('2.9') # For Mac it is tweaked and optimized with 2.9
    else:
        print "(1) wxPython-2.9 is not installed"

else:
    try:
        if wxversion.checkInstalled('2.8'):
            wxversion.select('2.8') # On MSW and GTK we stick with 2.8 for now
        else:
            print "(1) wxPython-2.8 is not installed"

    except:
        # continue anyways.
        # in the pyinstaller binary wxversion can screw up and throw exceptions
        # so we ignore the error and just use the wx that happens to be available.
        # TODO: Does this still happen since we now use checkInstalled()?
        print "(2) wxversion screwed up, this is harmless, ignoring it."# TODO: Does this still happen since we now use checkInstalled()?
        print "(2) wxversion screwed up, this is harmless, ignoring it."
        # TODO: Does this still happen since we now use checkInstalled()?
        print "(2) wxversion screwed up, this is harmless, ignoring it."
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
