from collections import namedtuple

import xbmc
import xbmcaddon

from ..logger import Logger

# Custom objects
AddonSettings = namedtuple('AddonSettings', ['dropbox_api_key', 'log_level', 'sync_group',
                                             'selective_sync', 'dry_run', 'sync_interval'])


def get_add_on_settings(add_on):
    """ Generic method that fetches all add-on settings

    :param add_on: the Kodi add-on object
    :return:       an AddonSettings namedtuple

    """

    # Map the settings index to the actual log level
    config_levels = [Logger.TRACE, Logger.DEBUG, Logger.INFO]

    log_level = config_levels[int(add_on.getSetting("log_level"))]
    dropbox_api_key = add_on.getSetting('dropbox_api_key')
    sync_group = add_on.getSetting('sync_group')
    dry_run = add_on.getSetting("dry_run") == "true"
    sync_interval = int(add_on.getSetting("sync_interval") or "5")

    sync_mode = add_on.getSetting('sync_mode')
    selective_sync = sync_mode == "1"

    return AddonSettings(dropbox_api_key=dropbox_api_key,
                         log_level=log_level,
                         sync_group=sync_group,
                         selective_sync=selective_sync,
                         dry_run=dry_run,
                         sync_interval=sync_interval)


def is_add_on_installed(add_on_id):
    installed = xbmc.getCondVisibility('System.HasAddon("%s")' % (add_on_id,)) == 1
    Logger.trace("Add-on '%s' is%s installed", add_on_id, "" if installed else " NOT")
    return installed


def can_add_on_sync(add_on_id):
    add_on = xbmcaddon.Addon(add_on_id=add_on_id)
    can_sync = add_on.getSetting("cloud_sync_enabled") == "true"
    Logger.trace("Add-on '%s' can%s sync", add_on_id, "" if can_sync else " NOT")
    return can_sync
