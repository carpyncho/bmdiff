#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


# =============================================================================
# DOCS
# =============================================================================

__doc__ = """Make a difference between two band merges"""

__version__ = "0.0.1"


# =============================================================================
# IMPORTS
# =============================================================================

import sys
import os
import argparse
import logging
import copy
import uuid
import warnings

import numpy as np

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from astropysics import coords


# =============================================================================
# LOG
# =============================================================================

logger = logging.getLogger("mmatch")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)


# =============================================================================
# CONSTANTS
# =============================================================================

DOC = __doc__

VERSION = __version__

EPILOG = "BSD-3 Licensed - IATE-OAC: http://iate.oac.uncor.edu/"

DEFAULT_RADIUS = 3 * 9.2592592592592588e-5

EPOCHS = 3


SOURCE_DTYPE = {
    'names': ['ra_h', 'dec_h', 'ra_j', 'dec_j', 'ra_k', 'dec_k'],
    'formats': [float, float, float, float, float, float]
}

USECOLS = [0, 1, 2, 3, 4, 5]


# =============================================================================
# MAIN
# =============================================================================

def read_bm(fp):
    logger.info("- Reading {}...".format(fp))

    arr = np.genfromtxt(
        fp, skip_header=EPOCHS,
        dtype=SOURCE_DTYPE,
        usecols=USECOLS)
    flt = (arr["ra_k"] > -9999.0)
    filtered = arr[flt]

    logger.info("Found {}/{} valid sources".format(len(arr), len(filtered)))

    return filtered


def match(bm0_ra, bm0_dec, bm1_ra, bm1_dec, radius=DEFAULT_RADIUS):
    logger.info("- Matching max distance of...".format(radius))

    nearestind_bm1, distance_bm1, match_bm1 = coords.match_coords(
        bm0_ra, bm0_dec, bm1_ra, bm1_dec, eps=radius, mode="nearest")

    nearestind_bm0, distance_bm0, match_bm0 = coords.match_coords(
        bm1_ra, bm1_dec, bm0_ra, bm0_dec, eps=radius, mode="nearest")

    for idx_bm1, idx_bm0 in enumerate(nearestind_bm0):
        if match_bm0[idx_bm1] and \
           nearestind_bm1[idx_bm0] == idx_bm1 \
           and match_bm1[idx_bm0]:
                yield idx_bm0, idx_bm1


def difference(ibm, flts, radius=DEFAULT_RADIUS, band="k"):
    ra, dec = "ra_{}".format(band), "dec_{}".format(band)

    to_remove = None
    for flt in flts:
        matches = np.fromiter(
            match(ibm[ra], ibm[dec], flt[ra], flt[dec], radius=radius),
            dtype=[("idx_ibm", int), ("idx_flt", int)])
        if to_remove is None:
            to_remove = matches["idx_ibm"]
        else:
            import ipdb; ipdb.set_trace()


    #~ remove_bm0 = np.unique(matches["idx_bm0"])
    #~ remove_bm1 = np.unique(matches["idx_bm1"])

    #~ np.concat


        import ipdb; ipdb.set_trace()



# =============================================================================
# MAIN
# =============================================================================

def _get_parser():
    parser = argparse.ArgumentParser(
        description=DOC, version=VERSION, epilog=EPILOG)

    parser.add_argument(
        'input', action='store', metavar="BAND-MERGE", help='Band-Merge file')

    parser.add_argument(
        '--filters', "-f", dest="filters", action='store', required=True,
        metavar="BAND-MERGE", nargs="+", help=(
            'Band-Merge file with the list of sources '
            'to be removed from input'))

    parser.add_argument(
        "--band", "-b", dest="band", action="store",
        default="k", choices="hjk", help="Radious to make the crossmatch")
    parser.add_argument(
        "--radius", "-r", dest="radius", action="store",
        default=DEFAULT_RADIUS, type=float,
        help="Radious to make the crossmatch")

    parser.add_argument(
        '--output', '-o', dest='output', action='store',
        type=argparse.FileType('w'), metavar="PATH",
        help='Destination of your difference')

    parser.add_argument(
        '--quiet', '-q', dest='loglevel', action='store_const',
        const=logging.WARNING, default=logging.INFO,
        help='Set log-level to warning')

    return parser


def _main(argv):

    # parse the arguments
    parser = _get_parser()
    args = parser.parse_args(argv)

    # extract and post-process the input data
    logger.setLevel(args.loglevel)

    # read the input
    logger.info("[INPUT]")
    inputbm = read_bm(args.input)

    logger.info("[FILTERS]")
    filters = map(read_bm, args.filters)

    # make difference
    diff = difference(inputbm, filters, radius=args.radius, band=args.band)



if __name__ == "__main__":
    _main(sys.argv[1:])
