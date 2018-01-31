#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import numpy as np

import bmdiff

bmdiff.logger.setLevel(logging.INFO)


def test_difference():
    print("TESTING DIFFERENCE")
    inputbm = bmdiff.read_bm("data/ibm.dat", "k")
    filters = [
        bmdiff.read_bm(flt, band="k")
        for flt in ("data/flt0.dat", "data/flt1.dat")]
    expected = np.loadtxt("data/diff.dat")

    diff = bmdiff.difference(inputbm, filters, band="k")
    for de, ee in zip(diff, expected):
        np.testing.assert_array_equal(
            np.asarray(de.tolist()), ee)


def test_union():
    print("TESTING UNION")
    bms = filters = [
        bmdiff.read_bm(flt, band="k")
        for flt in ("data/union0.dat", "data/union1.dat", "data/union2.dat")]
    expected = np.loadtxt("data/union.dat")

    union = bmdiff.union(bms, band="k")
    import ipdb; ipdb.set_trace()
    for de, ee in zip(union, expected):
        np.testing.assert_array_equal(
            np.asarray(de.tolist()), ee)
