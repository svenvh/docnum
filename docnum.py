#!/usr/bin/env python

import ConfigParser
import datetime
import os

class Config:
    '''Configuration/state.'''
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.configfile_used = self.config.read(['docnum.conf', os.path.expanduser('~/docnum.conf')])
        if not self.configfile_used:
            raise Exception('Cannot read config file')

    def get_prefix(self):
        '''Return prefix setting.'''
        return self.config.get('Settings', 'prefix')

    def get_next_id_and_inc(self):
        '''Return next ID and increment ID in config file.'''
        result = self.config.get('Data', 'next-id')
        next = int(result) + 1
        self.config.set('Data', 'next-id', next)
        outputfile = open(self.configfile_used[0], 'wb')
        self.config.write(outputfile)
        outputfile.close()
        return result

def get_dest_filename(config):
    '''Return destination filename.'''
    result = ''
    result += config.get_prefix()
    result += datetime.date.today().strftime("%Y-%m-%d")
    result += '-n'
    result += config.get_next_id_and_inc()
    return result

def main():
    '''Main entry point.'''
    config = Config()
    print get_dest_filename(config)

if __name__ == "__main__":
    main()
