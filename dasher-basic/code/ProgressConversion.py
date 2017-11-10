#  RUMBA
#  Copyright (C) 2017  Fundacio i2CAT, Internet i Innovacio digital a Catalunya
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  Authors:  Joan Llobera <joan.llobera@i2cat.net>, David Gómez <david.gomez@i2cat.net>




import math
import re
import subprocess


class ProgressConversion(object):
    """
    Usage:
        runner = FFMpegRunner()
        def status_handler(old, new):
            print "From {0} to {1}".format(old, new)
        runner.run('ffmpeg -i ...', status_handler=status_handler)
    """ 
    re_duration = re.compile('Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2})[^\d]*', re.U)
    re_position = re.compile('time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})\d*', re.U | re.I)
    horas = 0
    minutos = 0
    segundos =0

    def run_session(self, command, status_handler=None):
        pipe = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines = True)
        
        duration = None
        position = None
        percents = 0
        while True:
            line = pipe.stdout.readline().strip()
            if line == '' and pipe.poll() is not None:
                break

            if duration is None:
                duration_match = self.re_duration.match(line)
                if duration_match:
                    duration = self.time2sec(duration_match)
            if duration:
                position_match = self.re_position.search(line)
                if position_match:
                    position = self.time2sec(position_match)
            new_percents = self.get_percent(position, duration)
            if new_percents != percents:
                if callable(status_handler):
                    status_handler(percents, new_percents)
                percents = new_percents

    def get_percent(self, position, duration):
        if not position or not duration:
            return 0
        percent = int((100 * position / duration))
        return 100 if percent > 100 else percent

    def time2sec(self, search):
        return int(search.group(1))*3600 + int(search.group(2))*60 + int(search.group(3))                  
        #return sum([i**(2-i) * int(search.group(i+1)) for i in xrange(3)])
        
