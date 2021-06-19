import win32console, win32con, time
def main():
    #setup
    dims = (250, 70)
    world = []
    colormap = []
    row = ""
    for x in range(dims[0] * dims[1]):
        row += "f"
        if(x % 3 == 0):
            colormap.append(0x000C)
        else:
            colormap.append(0x0005)
    world.append(row)
    myConsole = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                                                       ShareMode=0,
                                                       SecurityAttributes=None,
                                                       Flags=1)
    myConsole.SetConsoleWindowInfo(Absolute=True,ConsoleWindow = win32console.PySMALL_RECTType(0,0,1,1))                                               
    myConsole.SetConsoleScreenBufferSize(win32console.PyCOORDType(dims[0],dims[1]))
    myConsole.SetConsoleWindowInfo(Absolute=True,ConsoleWindow = win32console.PySMALL_RECTType(0,0,dims[0]-1,dims[1]-1))  
    #myConsole.SetConsoleDisplayMode(Flags=win32console.CONSOLE_FULLSCREEN, NewScreenBufferDimensions = win32console.PyCOORDType(200,50))                                      
    myConsole.SetConsoleActiveScreenBuffer()
    myConsole.SetConsoleCursorInfo(Size=1,Visible=0)
    while True:
        # render world
        begin_time = time.time()
        myConsole.WriteConsoleOutputCharacter(world[0],win32console.PyCOORDType(0, 0))
        ms = 1000 * (time.time() - begin_time)
        time.sleep(0.5)
        win32console.SetConsoleTitle(f"{ms} ms")
if __name__ == "__main__":
    main()