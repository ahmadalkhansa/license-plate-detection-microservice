# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""License Plate Detection
This implementation does its best to follow the Robert Martin's Clean code guidelines.
The comments follows the Google Python Style Guide:
    https://github.com/google/styleguide/blob/gh-pages/pyguide.md
"""

__copyright__ = 'Copyright 2023, FCRlab at University of Messina'
__author__ = 'Lorenzo Carnevale <lcarnevale@unime.it>'
__credits__ = ''
__description__ = 'License Plate Detection'

import pika
import os
import yaml
import argparse
from threading import Lock
from logic.writer import Writer
from logic.reader import Reader

def main():
    description = ('%s\n%s' % (__author__, __description__))
    epilog = ('%s\n%s' % (__credits__, __copyright__))
    parser = argparse.ArgumentParser(
        description = description,
        epilog = epilog
    )

    parser.add_argument('-c', '--config',
                        dest='config',
                        help='YAML configuration file',
                        type=str,
                        required=True)

    parser.add_argument('-v', '--verbosity',
                        dest='verbosity',
                        help='Logging verbosity level',
                        action="store_true")
    
    parser.add_argument('-b', '--rhost',
                        help='RabbitMQ broker',
                        type=str,
                        required=True)

    parser.add_argument('-p', '--rport',
                        help='RabbitMQ listening port',
                        type=int,
                        required=True)
  
    parser.add_argument('-u', '--ruser',
                        help='RabbitMQ username',
                        type=str,
                        required=True)

    parser.add_argument('-s', '--rpassword',
                        help='RabbitMQ password',
                        type=str,
                        required=True)

    parser.add_argument('-q', '--rqueue',
                        help='RabbitMQ queue',
                        type=str,
                        required=True)

    options = parser.parse_args()
    verbosity = options.verbosity
    mutex = Lock()
    with open(options.config) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    logdir_name = config['logging']['logging_folder']
    logging_path = '%s/%s' % (config['logging']['logging_folder'], config['logging']['logging_filename'])
    if not os.path.exists(logdir_name):
        os.makedirs(logdir_name)

    writer = setup_writer(config['restful'], config['static_files'], mutex, verbosity, logging_path)
    reader = setup_reader(config['detection'], config['static_files'], mutex, verbosity, logging_path, options.rhost, options.rport, options.ruser, options.rpassword, options.rqueue)
    writer.start()
    reader.start()

def setup_writer(config, config_files, mutex, verbosity, logging_path):
    writer = Writer(config['host'], config['port'],
        config_files['potential'], mutex, verbosity, logging_path)
    writer.setup()
    return writer

def setup_reader(config, config_files, mutex, verbosity, logging_path, rhost, rport, user, password, queue):
    reader = Reader(config_files['potential'], config_files['detected'], config['model_path'], mutex, verbosity, logging_path, rhost, rport, user, password, queue)
    reader.setup()
    return reader

if __name__ == '__main__':
    main()
