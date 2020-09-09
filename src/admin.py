import sys, os, traceback, types

def isuseradmin():

    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False
    elif os.name == 'posix':
        return os.getuid() == 0
    else:
        raise RuntimeError("Unsupported operating system for this module: %s" % (os.name,))

def runasadmin(cmdline=None, wait=True):

    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon

    python_exe = sys.executable

    if cmdline is None:
        cmdline = [python_exe] + sys.argv
    elif type(cmdline) not in (types.TupleType,types.ListType):
        raise ValueError("cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdline[0],)
    params = " ".join(['"%s"' % (x,) for x in cmdline[1:]])
    showcmd = win32con.SW_SHOWNORMAL
    lpverb = 'runas'

    procinfo = ShellExecuteEx(nShow=showcmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpverb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        prochandle = procinfo['hProcess']
        rc = win32process.GetExitCodeProcess(prochandle)
    else:
        rc = None

    return rc

def test():
    rc = 0
    if not isuseradmin():
        print ("You're not an admin.", os.getpid(), "params: ", sys.argv)
        rc = runasadmin()
    else:
        print ("You are an admin!", os.getpid(), "params: ", sys.argv)
        rc = 0
    return rc


if __name__ == "__main__":
    sys.exit(test())