#!/usr/bin/env python
# -*- coding: utf-8
"""Entry point to the interactive interface for pan genomes.

The massage of the data is being taken care of in the interactive module,
and this file implements the bottle callbacks."""

import sys
#from anvio.argparse import ArgumentParser
import argparse
import anvio
import anvio.utils as utils
import anvio.terminal as terminal
import anvio.interactive as interactive
from django.http import Http404, JsonResponse, HttpResponse
from django.conf import settings
from anvio.bottleroutes import BottleApplication
from os.path import dirname
print(dirname(__file__))
from anvio.errors import ConfigError, FilesNPathsError, DictIOError, HDF5Error

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

__author__ = "Developers of anvi'o (see AUTHORS.txt)"
__copyright__ = "Copyleft 2015-2018, the Meren Lab (http://merenlab.org/)"
__credits__ = []
__license__ = "GPL 3.0"
__version__ = anvio.__version__
__maintainer__ = "A. Murat Eren"
__email__ = "a.murat.eren@gmail.com"
__requires__ = ['pan-db', 'genomes-storage-db']
__provides__ = ['collection', 'bin', 'interactive', 'svg']
__resources__ = [("See this program in action on the pangenomics tutorial", "http://merenlab.org/2016/11/08/pangenomics-v2/#displaying-the-pan-genome")]
__description__ = "Start an anvi'o server to display a pan-genome"

run = terminal.Run()
progress = terminal.Progress()
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Interactive():
    """Custom made"""
    def __init__(self, pan_db=None, genome_storage=None):

        if pan_db and genome_storage:
            args = {
              'pan_db': pan_db,
              'genomes_storage': genome_storage,
              'mode':'pan',
              'additional_layers':None,
              'additional_view':None,
              'browser_path':None,
              'collection_autoload':None,
              'dry_run':False,
              'export_svg':None,
              'ip_address':'localhost',
              'password_protected':False,
              'port_number':0,
              'read_only':False,
              'server_only':False,
              'skip_auto_ordering':False,
              'skip_init_functions':False,
              'skip_news':False,
              'state_autoload':None,
              'title':None,
              'tree':None,
              'user_server_shutdown':False,
              'view':None,
              'view_data':None
            }
            self.args = Struct(**args)

        else:


            # setup the command line user interface
            print('in displayAV run()')
            parser = argparse.ArgumentParser(description=__description__)

            groupA = parser.add_argument_group('INPUT FILES', "Input files from the pangenome analysis.")
            groupA.add_argument(*anvio.A('pan-db'), **anvio.K('pan-db', {'required': False}))
            groupA.add_argument(*anvio.A('genomes-storage'), **anvio.K('genomes-storage', {'required': False}))

            groupB = parser.add_argument_group('OPTIONAL INPUTS', "Where the yay factor becomes a reality.")
            groupB.add_argument(*anvio.A('view-data'), **anvio.K('view-data'))
            groupB.add_argument(*anvio.A('tree'), **anvio.K('tree'))

            groupC = parser.add_argument_group('ADDITIONAL STUFF', "Parameters to provide additional layers, views, or layer data.")
            groupC.add_argument(*anvio.A('additional-view'), **anvio.K('additional-view'))
            groupC.add_argument(*anvio.A('additional-layers'), **anvio.K('additional-layers'))

            groupD = parser.add_argument_group('VISUALS RELATED', "Parameters that give access to various adjustements regarding\
                                                                   the interface.")
            groupD.add_argument(*anvio.A('view'), **anvio.K('view'))
            groupD.add_argument(*anvio.A('title'), **anvio.K('title'))
            groupD.add_argument(*anvio.A('state-autoload'), **anvio.K('state-autoload'))
            groupD.add_argument(*anvio.A('collection-autoload'), **anvio.K('collection-autoload'))
            groupD.add_argument(*anvio.A('export-svg'), **anvio.K('export-svg'))

            groupE = parser.add_argument_group('SWEET PARAMS OF CONVENIENCE', "Parameters and flags that are not quite essential (but\
                                                                               nice to have).")
            groupE.add_argument(*anvio.A('skip-init-functions'), **anvio.K('skip-init-functions'))
            groupE.add_argument(*anvio.A('dry-run'), **anvio.K('dry-run'))
            groupE.add_argument(*anvio.A('skip-auto-ordering'), **anvio.K('skip-auto-ordering'))
            groupE.add_argument(*anvio.A('skip-news'), **anvio.K('skip-news'))

            groupF = parser.add_argument_group('SERVER CONFIGURATION', "For power users.")
            groupF.add_argument(*anvio.A('ip-address'), **anvio.K('ip-address'))
            groupF.add_argument(*anvio.A('port-number'), **anvio.K('port-number'))
            groupF.add_argument(*anvio.A('browser-path'), **anvio.K('browser-path'))
            groupF.add_argument(*anvio.A('read-only'), **anvio.K('read-only'))
            groupF.add_argument(*anvio.A('server-only'), **anvio.K('server-only'))
            groupF.add_argument(*anvio.A('password-protected'), **anvio.K('password-protected'))
            groupF.add_argument(*anvio.A('user-server-shutdown'), **anvio.K('user-server-shutdown'))
            print('in displayAV run()2a')
            args = parser.parse_args()
            #args = parser.get_args(parser)  #, auto_fill_anvio_dbs=True)
            print('in displayAV run()3')
            self.args = args
            print('Default ARGS')
            self.args.mode = 'pan'
            setattr(self.args, 'new', 'newarg')
            print(self.args)

    def run_app(self):
            try:

                d = interactive.Interactive(self.args)

                self.args.port_number = utils.get_port_num(self.args.port_number, self.args.ip_address, run=run)
            except ConfigError as e:
                print(e)
                sys.exit(-1)
            except FilesNPathsError as e:
                print(e)
                sys.exit(-2)
            except DictIOError as e:
                print(e)
                sys.exit(-3)
            except HDF5Error as e:
                print(e)
                sys.exit(-4)

            if self.args.dry_run:
                run.info_single('Dry run? Kthxbai.', nl_after=1, nl_before=1)
                sys.exit()
            print('Default d')
            print(d)
            app = BottleApplication(d)
            logger.debug('got bottleapp')
            
            
            logger.debug('URL: http://'+self.args.ip_address+':'+str(self.args.port_number) )
            
            #http://0.0.0.0:8081/app/index.html?rand=e621857f
            return (app, self.args)
            
    

if __name__ == '__main__':

    print('in if __name__ == "__main__"')

    I = Interactive()
    (app, args) = I.run_app()
    #app.run_application(args.ip_address, args.port_number)
    #application = app.default_app()
    #HttpResponse(app.get_news(), content_type='application/json')

    app.run_application(args.ip_address, args.port_number)
