import pathlib
import os
import flask

_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''

_USER_PAGE_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {messages}
        </table>
    </body>
</html>
'''

_MESSAGE_LINE_HTML = '''
<tr>
    <td>{time}</td>
    <td>{message}</td>
<tr>
'''

app = flask.Flask(__name__)
# A global variable holding the current data directory entered by the user.
glob_data_dir = None


def run_webserver(address, data_dir):
    global glob_data_dir
    glob_data_dir = pathlib.Path(data_dir)
    if type(address) == str:
        ip, port = address.split(':')
    else: # it's a tuple
        ip, port = address
    app.run(host=ip, port=int(port))


@app.route('/')
def index():
    global glob_data_dir
    users_html = []
    for user_dir in glob_data_dir.iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return index_html, 200


@app.route('/users/<user_id>')
def user(user_id):
    if not user_id.isdigit():
        return '', 404

    global glob_data_dir
    users_ids = [user_dir.name for user_dir in glob_data_dir.iterdir()]
    if user_id in users_ids:
        messages_html = []
        # The last member in the split version of the page will be user_id.
        user_dir_name = os.path.join(glob_data_dir.name, user_id)
        user_dir = pathlib.Path(user_dir_name)
        for time_file in user_dir.iterdir():
            for message in time_file.open().read().splitlines():
                date, hours = time_file.name.split("_")
                formatted_hours = hours.replace("-", ":").replace(".txt", "")
                formatted_time = date + " " + formatted_hours
                msg_fmt = _MESSAGE_LINE_HTML.format(time=formatted_time,
                                                    message=message+'\n')
                messages_html.append(msg_fmt)
        user_html = _USER_PAGE_HTML.format(user_id=user_id,
                                           messages='\n'.join(messages_html))
        return user_html, 200
    # Else, there's no such user in the system,
    # and we should send an error code.
    return '', 404


def main(argv):
    if len(argv) != 3:
        print("usage: {0} <address> <data directory>".format(argv[0]))
        return 1

    try:
        ip, port = argv[1].split(":")
        data_dir = pathlib.Path(argv[2])
        run_webserver((ip, int(port)), data_dir)
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
