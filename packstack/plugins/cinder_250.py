"""
Installs and configures Cinder
"""

import logging

import packstack.installer.engine_validators as validate
from packstack.installer import basedefs
import packstack.installer.common_utils as utils

from packstack.modules.ospluginutils import getManifestTemplate, appendManifestFile

# Controller object will be initialized from main flow
controller = None

# Plugin name
PLUGIN_NAME = "OS-Cinder"
PLUGIN_NAME_COLORED = utils.getColoredText(PLUGIN_NAME, basedefs.BLUE)

logging.debug("plugin %s loaded", __name__)

def initConfig(controllerObject):
    global controller
    controller = controllerObject
    logging.debug("Adding Openstack Cinder configuration")
    paramsList = [
                  {"CMD_OPTION"      : "cinder-host",
                   "USAGE"           : "The IP address of the server on which to install Cinder",
                   "PROMPT"          : "The IP address of the server on which to install Cinder",
                   "OPTION_LIST"     : [],
                   "VALIDATION_FUNC" : validate.validatePing,
                   "DEFAULT_VALUE"   : "127.0.0.1",
                   "MASK_INPUT"      : False,
                   "LOOSE_VALIDATION": True,
                   "CONF_NAME"       : "CONFIG_CINDER_HOST",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                 ]

    groupDict = { "GROUP_NAME"            : "CINDER",
                  "DESCRIPTION"           : "Cinder Config paramaters",
                  "PRE_CONDITION"         : "CONFIG_CINDER_INSTALL",
                  "PRE_CONDITION_MATCH"   : "y",
                  "POST_CONDITION"        : False,
                  "POST_CONDITION_MATCH"  : True}

    controller.addGroup(groupDict, paramsList)


def initSequences(controller):
    if controller.CONF['CONFIG_CINDER_INSTALL'] != 'y':
        return

    cindersteps = [
             {'title': 'Adding Cinder Keystone Manifest entries', 'functions':[createkeystonemanifest]},
             {'title': 'Checking if the Cinder server has a cinder-volumes vg', 'functions':[checkcindervg]},
             {'title': 'Creating Cinder Manifest', 'functions':[createmanifest]}
    ]
    controller.addSequence("Installing Cinder", [], [], cindersteps)

def checkcindervg():
    server = utils.ScriptRunner(controller.CONF['CONFIG_CINDER_HOST'])
    server.append('vgdisplay cinder-volumes')
    try:
        server.execute()
    except:
        print "The cinder server should contain a cinder-volumes volume group"
        raise

def createkeystonemanifest():
    manifestfile = "%s_keystone.pp"%controller.CONF['CONFIG_KEYSTONE_HOST']
    manifestdata = getManifestTemplate("keystone_cinder.pp")
    appendManifestFile(manifestfile, manifestdata)

def createmanifest():
    manifestfile = "%s_cinder.pp"%controller.CONF['CONFIG_CINDER_HOST']
    manifestdata = getManifestTemplate("cinder.pp")
    appendManifestFile(manifestfile, manifestdata)

