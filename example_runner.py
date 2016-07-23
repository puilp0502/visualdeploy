import cherrypy
import cherrypy.wsgiserver
from stream import app

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 9000,
                       })
#server = cherrypy.wsgiserver.CherryPyWSGIServer('0.0.0.0', app, timeout=100)
tree = cherrypy.tree.graft(app, '/')

cherrypy.engine.start()
cherrypy.engine.block()
#cherrypy.quickstart(server, '/')
