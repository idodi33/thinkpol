from flask import Flask, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.routing import BaseConverter



class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        self.regex = items[0]
        super(RegexConverter, self).__init__(url_map)



def run_gui_server(gui_host, gui_port, api_host, api_port):
    """
    Receives address of api server and desired gui server and starts serving information
    from the react application we built using flask.
    :param gui_host: gui host
    :type gui_host: str
    :param gui_port: gui port
    :type gui_port: int
    :param api_host: api host
    :type api_host: str
    :param api_port: api port
    :type api_port: int
    """
    gui = Flask(__name__, static_folder="../../gui/build/static", template_folder="../../gui/build")
    gui.url_map.converters['regex'] = RegexConverter
    CORS(gui)

    @gui.route('/', defaults={'path': ''})
    @gui.route('/<path:path>')
    def handle(path):
        response = render_template("index.html", api_url=f"http://{api_host}:{api_port}")
        return response

    @gui.route("/<regex(r'(.*?)\.(png|PNG|ico|js)$'):file>", methods=["GET"])
    def handle_public(file):
        """FLASK FUNCITON
        Routes to all resources in the react public folder.
        
        :param file: filename from /public
        :type file: str
        """
        return send_from_directory("../../gui/build", file)

    gui.run(host=gui_host, port=gui_port)