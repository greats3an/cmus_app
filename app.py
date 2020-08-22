#!/usr/bin/env python
'''
https://github.com/jboynyc/cmus_app
'''
# =======================================================================
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
# =======================================================================


from optparse import OptionParser
from re import sub
from typing import DefaultDict
from bottle import abort, post, request, response, route, run, view, static_file
import subprocess

hostname = subprocess.run('hostname', capture_output=True)
hostname = hostname.stdout.decode()

class NoConnectionError(Exception):
    '''Raised when falied to connect to cmus'''
    pass


class RemoteClass:

    def __call__(self, *args):
        process = subprocess.run(['cmus-remote', *args], capture_output=True)
        assert process.returncode == 0
        return process

    def __init__(self) -> None:
        # Check if is cmus alive
        try:
            self.__call__('-Q')
        except:
            raise NoConnectionError(
                "Unable to establish connection to cmus via UNIX socket")


class ConfigFileNotFound(IOError):
    '''Raised when the specified config file does not exist or is empty.'''
    pass


class MissingSetting(Exception):
    '''Raised when the config file is missing a required setting.'''
    pass


@route('/audio/<file>')
def audio(file):
    if settings['disable_streaming']:
        print('Streaming is disabled')
        return {}
    file = file.replace('|','/')
    print('Requesting local file',file)
    return static_file(file,'/')
@route('/')
@view('main')
def index():
    return {'host': hostname,'welcome':settings['welcome']}

@post('/cmd')
def run_command():
    legal_commands = {'Play': 'player-play',
                      'Pause': 'player-pause',
                      'Next': 'player-next',
                      'Previous': 'player-prev',
                      'Increase Volume': 'vol +10%',
                      'Reduce Volume': 'vol -10%',
                      'Mute': 'vol 0',
                      'Step -5s': 'seek -5',
                      'Step +5s': 'seek +5',
                      'Toggle Shuffle' : 'toggle shuffle'
                      }
    command = request.POST.get('command', default=None)
    if command in legal_commands:
        try:
            out = Remote('-C', legal_commands[command])
            return {'result': out.returncode, 'output': out.stdout.decode()}
        except NoConnectionError:
            abort(503, 'Cmus not running.')
    else:
        abort(400, 'Invalid command.')


@route('/status')
def get_status():
    try:
        process = subprocess.run(['cmus-remote', '-Q'], capture_output=True)
        if not process.returncode == 0:
            return {}
        else:
            result = DefaultDict(list)
            for k, v in [(l[:l.index(' ')], l[l.index(' ') + 1:]) for l in process.stdout.decode().split('\n') if ' ' in l]:
                result[k].append(v)
            for k in ['tag', 'set']:
                result[k] = {s.split(' ')[0]: s[len(
                    s.split(' ')[0]) + 1:] for s in result[k]}
            return result
    except NoConnectionError:
        abort(503, 'Cmus not running.')


@route('/static/<file>')
def static(file):
    response.set_header('Cache-Control', 'max-age=604800')
    return static_file(file, root='static')


@route('/favicon.ico')
def favicon():
    response.set_header('Cache-Control', 'max-age=604800')
    return static_file('favicon.ico', root='static')


if __name__ == '__main__':
    option_parser = OptionParser()
    option_parser.add_option('-a', '--app-host', dest='app_host',
                             help='Name of cmus_app host.',
                             default='localhost')
    option_parser.add_option('-p', '--app-port', dest='app_port',
                             help='Port cmus_app is listening on.',
                             default=8080)
    option_parser.add_option('--disable-streaming',dest='disable_streaming',
                             help='Disable internal streaming',
                             action='store_true')                
    option_parser.add_option('--welcome',dest='welcome',
                             help='Welcome Message',
                             default='Hello there')                                                 
    options, _ = option_parser.parse_args()
    settings = vars(options)
    Remote = RemoteClass()

    print("Bottle is now listening on http://%s:%s/\n" % (settings['app_host'], settings['app_port']))
    run(host=settings['app_host'], port=int(settings['app_port']),server='auto')
