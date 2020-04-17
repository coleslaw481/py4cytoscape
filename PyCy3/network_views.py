# -*- coding: utf-8 -*-

"""Functions for performing VIEW operations in addition to getting and setting view properties.

Dev Notes: refer to StyleValues.R, StyleDefaults.R and StyleBypasses.R for
getting/setting node, edge and network visual properties via VIEW operations.
"""

import sys
import os

from . import commands
from . import networks
from .exceptions import CyError
from .pycy3_utils import *

def get_network_views(network=None, base_url=DEFAULT_BASE_URL):
    """Retrieve list of network view SUIDs.

    Args:
        network (str or SUID or None): Name or SUID of the network. Default is the "current" network active in Cytoscape.
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of PyCy3.

    Returns:
        list: [list of SUIDs of views] where the list has length 1

    Raises:
        CyError: if network doesn't exist
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        >>> get_network_views()
        [130223]
        >>> get_network_views(51)
        [130223]
        >>> get_network_views(network='galFiltered.sif')
        [130223]
    """
    net_suid = networks.get_network_suid(network, base_url=base_url)
    res = commands.cyrest_get("networks/" + str(net_suid) + "/views", base_url=base_url)
# TODO: Note that we get a 404 exception here if there are no networks. Is that what we want?
    return res

def get_network_view_suid(network=None, base_url=DEFAULT_BASE_URL):
    """Retrieve the SUID of a network view.

    Args:
        network (str or SUID or None): Name or SUID of the network or view. Default is the "current" network active in Cytoscape.
            If a network view SUID is provided, then it is validated and returned.
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of PyCy3.

    Returns:
        int: SUID of the view for the network. The first (presummably only) view associated a network is returned.

    Raises:
        CyError: if network or view doesn't exist
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        >>> get_network_view_suid()
        130223
        >>> get_network_view_suid(51)
        130223
        >>> get_network_view_suid(network='galFiltered.sif')
        130223

    Dev Notes:
        analogous to getNetworkSuid, this function attempts to handle all of the multiple ways we support network view referencing (e.g., title, SUID, 'current', and NULL). These functions are then used by functions that take a "network" argument and requires a view SUID.
"""
    if isinstance(network, str):
        # network name (or "current") was provided, warn if multiple view
        network_views = get_network_views(network, base_url=base_url)
        if len(network_views) > 1:
            print('Warning: This network has multiple views. Returning last.')
        return network_views[-1]
    elif isinstance(network, int):
        # suid provided, but is it a network or a view?
        net_suids = commands.cyrest_get('networks', base_url=base_url)
        if network in net_suids: # network SUID, warn if multiple view
            network_views = get_network_views(network, base_url=base_url)
            if len(network_views) > 1:
                print('Warning: This network has multiple views. Returning last.')
            return network_views[-1]
        else:
            view_suids = [get_network_views(x, base_url=base_url)[0]   for x in net_suids]
            if network in view_suids: # view SUID, return it
                return network
            else:
                raise CyError('Network view does not exist for: ' + str(network))
    else:
        # use current network, return first view
        # TODO: R sets this but never uses it ...is this an error?
        network_title = 'current'
        # warn if multiple views
        network_views = get_network_views(network, base_url=base_url)
        if len(network_views) > 1:
            print('Warning: This network has multiple views. Returning last.')
        return network_views[-1]

def fit_content(selected_only=False, network=None, base_url=DEFAULT_BASE_URL):
    """Zoom and pan network view to maximize either height or width of current network window.

    Takes first (presumably only) view associated with provided network

    Args:
        selected_only (bool): Whether to fit only current selection. Default is false, i.e., to fit the entire network
        network (str or SUID or None): Name or SUID of the network or view. Default is the "current" network active in Cytoscape.
            If a network view SUID is provided, then it is validated and returned.
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of PyCy3.

    Returns:
        dict: {}

    Raises:
        CyError: if network or view doesn't exist
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        >>> fit_content()
        {}
        >>> fit_content(51, selected_only=True)
        {}
        >>> fit_content(network='galFiltered.sif')
        {}
    """
    view_suid = get_network_view_suid(network, base_url=base_url)
    if selected_only:
        res = commands.commands_post('view fit selected view=SUID:' + str(view_suid), base_url=base_url)
    else:
        res = commands.commands_post('view fit content view=SUID:' + str(view_suid), base_url=base_url)
    return res

def set_current_view(network=None, base_url=DEFAULT_BASE_URL):
    """Set which network view is "current".

    Takes first (presumably only) view associated with provided network

    Args:
        network (str or SUID or None): Name or SUID of the network or view. Default is the "current" network active in Cytoscape.
            If a network view SUID is provided, then it is validated and returned.
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of PyCy3.

    Returns:
        dict: {}

    Raises:
        CyError: if network or view doesn't exist
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        >>> set_current_view()
        {}
        >>> set_current_view(51)
        {}
        >>> set_current_view(network='galFiltered.sif')
        {}
    """
    view_suid = get_network_view_suid(network, base_url=base_url)
    res = commands.commands_post('view set current view=SUID:"' + str(view_suid) + '"', base_url=base_url)
    return res

# TODO: Need parameter to automatically overwrite file if it exists
def export_image(filename=None, type='PNG', resolution=None, units=None, height=None, width=None, zoom=None, network=None, base_url=DEFAULT_BASE_URL):
    """ Save the current network view as an image file.

    The image is cropped per the current view in Cytoscape. Consider applying :meth:`fit_content` prior to export.

    Args:
        filename (str): Full path or path relavtive to current working directory, in addition to the name of the file.
            Extension is automatically added based on the ``type`` argument. If blank, the current network name will be used.
        type (str): Type of image to export, e.g., PNG (default), JPEG, PDF, SVG, PS (PostScript).
        resolution (int): The resolution of the exported image, in DPI. Valid only for bitmap formats, when the selected
            width and height 'units' is inches. The possible values are: 72 (default), 100, 150, 300, 600.
        units (str) The units for the 'width' and 'height' values. Valid only for bitmap formats, such as PNG and JPEG.
            The possible values are: pixels (default), inches.
        height (float): The height of the exported image. Valid only for bitmap formats, such as PNG and JPEG.
        width (float): The width of the exported image. Valid only for bitmap formats, such as PNG and JPEG.
        zoom (float): The zoom value to proportionally scale the image. The default value is 100.0. Valid only for bitmap
            formats, such as PNG and JPEG
        network (str or SUID or None): Name or SUID of the network or view. Default is the "current" network active in Cytoscape.
            If a network view SUID is provided, then it is validated and returned.
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of PyCy3.

    Returns:
        dict:  {'file': name of file} contains absolute path to file that was written

    Raises:
        CyError: if network or view doesn't exist
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        >>> export_image('output/test', type='JPEG', units='pixels', height=1000, width=2000, zoom=200)
        {"file": "C:\\Users\\CyDeveloper\\tests\\output\\test.jpeg"
        >>> export_image('output/test', type='PDF', network='My Network')
        {"file": "C:\\Users\\CyDeveloper\\tests\\output\\test.pdf"
        >>> export_image(type='PNG', resolution=600, units='inches', height=1.7, width=3.5, zoom=500, network=13098)
        {"file": "C:\\Users\\CyDeveloper\\tests\\output\\test.png"
    """
    cmd_string = 'view export'  # a good start

    # filename must be supplied
    if not filename: filename = networks.get_network_name(network, base_url=base_url)

    # view must be supplied
    view_SUID = get_network_view_suid(network, base_url=base_url)

    # optional args
    if resolution: cmd_string += ' Resolution="' + str(resolution) + '"'
    if units: cmd_string += ' Units="' + str(units) + '"'
    if height: cmd_string += ' Height="' + str(height) + '"'
    if width: cmd_string += ' Width="' + str(width) + '"'
    if zoom: cmd_string += ' Zoom="' + str(zoom) + '"'

# TODO: It looks like the '.' should be escaped ... true?
# TODO: If a lower case comparison is going to be done, shouldn't filename also be lower-case?
    if re.search('.' + type.lower() + '$', filename) is None: filename += '.' + type.lower()
    filename = os.path.abspath(filename)
    if os.path.isfile(filename): print('This file already exists. A Cytoscape popup will be generated to confirm overwrite.')
    res = commands.commands_post(cmd_string + ' OutputFile="' + filename + '"' + ' options="' + type.upper() + '"' + ' view=SUID:"' + str(view_SUID) + '"', base_url=base_url)
    return res

def toggle_graphics_details(base_url=DEFAULT_BASE_URL):
    """Toggle Graphics Details.

    Regardless of the current zoom level and network size, show (or hide) graphics details, e.g., node labels.

    Displaying graphics details on a very large network will affect pan and zoom performance, depending on your available RAM.
    See :meth:`cytoscape_memory_status`.

    Args:
        network (str or SUID or None): Name or SUID of the network or view. Default is the "current" network active in Cytoscape.
            If a network view SUID is provided, then it is validated and returned.
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of PyCy3.

    Returns:
        dict: {'message': 'Toggled Graphics level of details.'}

    Raises:
        CyError: if network or view doesn't exist
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        >>> toggle_graphics_details()
        {'message': 'Toggled Graphics level of details.'}
    """
    res = commands.cyrest_put('ui/lod', base_url=base_url)
    return res
