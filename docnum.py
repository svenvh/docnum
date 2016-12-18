#!/usr/bin/env python

# Copy a file and number the copy, as specified in a configuration file.

import ConfigParser
import datetime
import os
import shutil

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

    def get_source(self):
        '''Return source file setting.'''
        return self.config.get('Settings', 'source')

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
    src_file = config.get_source()
    dst_file = get_dest_filename(config)
    if os.path.exists(dst_file):
        raise Exception('Destination file ' + dst_file + ' already exists!')
    print src_file + ' -> ' + dst_file
    shutil.copyfile(src_file, dst_file)

if __name__ == "__main__":
    main()
