import os
import subprocess

def execute(commands, head=None, post_run=None, error_color='00e676', success_color='e57373', hide_homedir=True):
    if head is None:
        head = """
    <head>
        <script type="text/javascript" src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
        <title>DynDeploy</title>
    </head>"""
    if post_run is None:    
        post_run = """
    window.scroll(0, document.body.scrollHeight);
    $("#output-%s").css({"background-color": "#%s"});
    """

    home = os.getenv('HOME')
    
    if hide_homedir: 
        def getcwd():  # Prevent absolute path from showing
            return os.getcwd().replace(home, '~')
    else:
        getcwd = os.getcwd

    yield '<html>'+head+'<body><h1>DynamicDeploy</h1>'
    
    for i, cmd in enumerate(commands):
        is_secret = False
        cmd = cmd.replace('~', home) # '~' shortcut doesn't work with os-like funcions
        
        if cmd[0] == '-':  # Check if command is hidden
            cmd = cmd[1:]
            is_secret = True

        if not is_secret: yield '<div id="output-{i}">'.format(i=i)

        if cmd[0:2] == "cd":  # cd doesn't work; we need to use chdir
            os.chdir(cmd[2:].strip())
            if not is_secret: yield '<div>Changing directory to: '+getcwd()+'</div>'
            continue

        if not is_secret:
            yield '<div style="background-color: black; color: white; font-family: monospace;">deploy@localhost:'+getcwd()+'$ '+cmd+'<br>'
        print(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        if is_secret:  # Secret commands don't need I/O handling
            proc.wait()
            continue

        for line in proc.stdout:
            line = line.decode('utf-8').replace('\n', '<br>').encode('utf-8')
            yield line
        proc.stdout.close()
        ret_code = proc.wait()

