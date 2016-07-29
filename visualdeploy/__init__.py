import os
import subprocess

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException


def execute(commands, head=None, post_run=None, success_color='00e676', error_color='e57373', hide_homedir=True):
    if head is None:
        head = """
    <head>
        <script type="text/javascript">
            function $(selector){
                return document.querySelector(selector);
            }
        </script>
        <title>VisualDeploy</title>
        <style>body{font-family: sans-serif;}</style>
    </head>"""
    if post_run is None:    
        post_run = """
    <script>
        window.scroll(0, document.body.scrollHeight);
        $("#output-{i}").style.backgroundColor = "#{color}";
    </script>
    """

    home = os.getenv('HOME')
    
    if hide_homedir: 
        def getcwd():  # Prevent absolute path from showing
            return os.getcwd().replace(home, '~')
    else:
        getcwd = os.getcwd

    yield '<html>'+head+'<body><h1>DynamicDeploy</h1>'
    
    i = 1
    for cmd in commands:
        is_secret = False
        cmd = cmd.replace('~', home) # '~' shortcut doesn't work with os-like funcions
        
        if cmd[0] == '-':  # Check if command is hidden
            cmd = cmd[1:]
            is_secret = True

        if not is_secret: yield '<div id="output-{i}">'.format(i=i)

        if cmd[0:2] == "cd":  # cd doesn't work; we need to use chdir
            os.chdir(cmd[2:].strip())
            if not is_secret: yield '<div>Changing directory to: '+getcwd()+'</div></div><hr/>'
            i += 1
            continue

        if not is_secret:
            yield '<div style="background-color: black; color: white; font-family: monospace;">deploy@localhost:'+getcwd()+'$ '+cmd+'<br>'
        print(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        if is_secret:  # Secret commands don't need any further processing
            proc.wait()
            continue

        for line in proc.stdout:
            line = line.decode('utf-8', errors='ignore').replace('\n', '<br>').encode('utf-8')
            yield line
        proc.stdout.close()
        ret_code = proc.wait()
        color = success_color if ret_code == 0 else error_color
        yield "</div><h4>Process returned: "+str(ret_code)+"</h4>"
        yield post_run.replace('{i}', str(i)).replace('{color}', str(color))
        yield "</div><hr/>"
        i += 1
    yield "<h3>Deploy Completed!</h3>"


def make_app(commands, deploy_route="/stream"):
    class VD(object):
        def __init__(self, commands):
            self.url_map = Map([
                Rule(deploy_route, endpoint='stream')
            ])
            self.commands = commands
        def dispatch_request(self, request):
            adapter = self.url_map.bind_to_environ(request.environ)
            try:
                endpoint, values = adapter.match()
                if endpoint == 'stream':
                    return Response(execute(self.commands), mimetype='text/html')
            except HTTPException as e:
                return e
        def wsgi_app(self, environ, start_response):
            request = Request(environ)
            response = self.dispatch_request(request)
            return response(environ, start_response)
        def __call__(self, environ, start_response):
            return self.wsgi_app(environ, start_response)
    app = VD(commands)
    return app

