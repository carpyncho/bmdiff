#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


# =============================================================================
# DOCS
# =============================================================================

__doc__ = """Make band merges difference and union."""

__version__ = "0.0.2"


# =============================================================================
# IMPORTS
# =============================================================================

import sys
import argparse
import logging
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

FORMATS = ['%i', '%1.18e', '%1.18e', '%1.18e', '%1.18e', '%1.18e', '%1.18e']


# =============================================================================
# MAIN
# =============================================================================

def add_columns(arr, extra_cols, append=False):
    """Add extra columns to the output of beamc"""

    dtype = (
        [(k, v.dtype) for k, v in extra_cols] +
        [(n, f) for n, f in arr.dtype.descr])

    extra_cols = dict(extra_cols)

    # create an empty array and copy the values
    data = np.empty(len(arr), dtype=dtype)
    for name in data.dtype.names:
        if name in extra_cols:
            data[name] = extra_cols[name]
        else:
            data[name] = arr[name]

    return data


def read_bm(fp, band="k", **kwargs):
    logger.info("- Reading {}...".format(fp))

    kwargs.setdefault("dtype", SOURCE_DTYPE)
    kwargs.setdefault("skip_header", EPOCHS)
    kwargs.setdefault("usecols", USECOLS)

    arr = np.genfromtxt(fp, **kwargs)
    if arr.ndim == 0:
        arr = arr.flatten()
    indexed = add_columns(arr, [("idx", np.arange(len(arr)))])

    ra = "ra_{}".format(band)
    flt = (indexed[ra] != -9999.0)
    filtered = indexed[flt]

    logger.info("Found {}/{} valid sources".format(len(filtered), len(arr)))
    return filtered


def match(bm0_ra, bm0_dec, bm1_ra, bm1_dec, radius=DEFAULT_RADIUS):
    logger.info("- Matching max distance of radius {}...".format(radius))
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
    logger.info("[MATCH]")
    for flt in flts:

        matches = np.fromiter(
            match(ibm[ra], ibm[dec], flt[ra], flt[dec], radius=radius),
            dtype=[("idx_ibm", int), ("idx_flt", int)])
        logger.info("Found {} sources matches".format(len(matches)))

        if to_remove is None:
            to_remove = matches["idx_ibm"]
        else:
            to_remove = np.append(to_remove, matches["idx_ibm"])

    logger.info("[FILTERING]")
    uto_remove = np.unique(to_remove)
    logger.info("{} unique sources to remove".format(len(uto_remove)))

    clean_mask = ~np.in1d(np.arange(len(ibm)), uto_remove)
    return ibm[clean_mask]


def union(bms, radius=DEFAULT_RADIUS, band="k"):
    ra, dec = "ra_{}".format(band), "dec_{}".format(band)
    united = None
    for idx, bm in enumerate(bms):
        bm_idx = np.zeros(len(bm), dtype=int) + idx
        bm = add_columns(bm, [("bm_idx", bm_idx)])
        if united is None:
            united = bm
        else:
            matches = np.fromiter(
                match(united[ra], united[dec], bm[ra], bm[dec], radius=radius),
                dtype=[("idx_united", int), ("idx_bm", int)])
            logger.info("Found {} sources matches".format(matches.size))
            logger.info("Filtering...")

            clean_mask = ~np.in1d(bm["idx"], matches["idx_bm"])
            united = np.append(united, bm[clean_mask])

    return united
