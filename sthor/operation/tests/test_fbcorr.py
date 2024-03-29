"""Test Suite for Filterbank Correlation Operation."""

# TODO: complete the test suite.

# Authors: Nicolas Pinto <nicolas.pinto@gmail.com>
#          Nicolas Poilvert <nicolas.poilvert@gmail.com>
#
# License: BSD

from nose.tools import raises
from nose.tools import assert_raises
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from numpy.testing import assert_allclose

import numpy as np
from scipy.misc import lena

from sthor.operation.fbcorr import fbcorr

# -- Raise exceptions on floating-point errors
np.seterr(all='raise')

# -- Global Variables
DTYPE = np.float32
RTOL = 1e-3
ATOL = 1e-6

# -----------------------------------------------------------------------------
# -- Unit Tests
# -----------------------------------------------------------------------------

def test_input_d_1():

    arr_in = np.zeros((2, 3, 1), dtype=DTYPE)
    arr_fb = np.zeros((4, 1, 1, 1), dtype=DTYPE)
    arr_out = np.zeros((2, 3, 4), dtype=DTYPE)

    arr_in[:] = np.arange(np.prod(arr_in.shape)).reshape(arr_in.shape)
    arr_fb[:] = np.arange(np.prod(arr_fb.shape)).reshape(arr_fb.shape)

    gt = np.array([[[  0.,   0.,   0.,   0.],
                    [  0.,   1.,   2.,   3.],
                    [  0.,   2.,   4.,   6.]],

                   [[  0.,   3.,   6.,   9.],
                    [  0.,   4.,   8.,  12.],
                    [  0.,   5.,  10.,  15.]]], dtype=DTYPE)

    fbcorr(arr_in, arr_fb, arr_out=arr_out)
    assert_allclose(arr_out[:], gt, rtol=RTOL, atol=ATOL)

    arr_out = fbcorr(arr_in, arr_fb)
    assert_allclose(arr_out[:], gt, rtol=RTOL, atol=ATOL)


def test_one_dot():

    arr_in = np.zeros((3, 3, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 3, 3, 4), dtype=DTYPE)
    arr_out = np.zeros((1, 1, 8), dtype=DTYPE)

    arr_in[:] = np.arange(np.prod(arr_in.shape)).reshape(arr_in.shape)
    arr_fb[:] = np.arange(np.prod(arr_fb.shape)).reshape(arr_fb.shape)

    gt = np.array([[[  14910.,   37590.,   60270.,   82950.,
                       105630.,  128310., 150990.,  173670.]]],
                  dtype=DTYPE)

    fbcorr(arr_in, arr_fb, arr_out=arr_out)
    assert_allclose(arr_out[:], gt, rtol=RTOL, atol=ATOL)

    arr_out = fbcorr(arr_in, arr_fb)
    assert_allclose(arr_out[:], gt, rtol=RTOL, atol=ATOL)


def test_arr_out_2d():

    arr_in = np.zeros((20, 30), dtype=DTYPE)
    arr_fb = np.zeros((8, 3, 3), dtype=DTYPE)
    arr_out = np.zeros((18, 28, 8), dtype=DTYPE)

    arr_in[:] = np.arange(np.prod(arr_in.shape)).reshape(arr_in.shape)
    arr_fb[:] = np.arange(np.prod(arr_fb.shape)).reshape(arr_fb.shape)

    gt = np.array([[  4182.,  12363.,  20544.,  28725.,
                     36906.,  45087.,  53268.,  61449.]
                   ,
                   [  5334.,  16107.,  26880.,  37653.,
                    48426.,  59199.,  69972.,   80745.]],
                  dtype=DTYPE)
    idx = [2, 3], [10, 12]

    fbcorr(arr_in, arr_fb, arr_out=arr_out)
    gv = arr_out[idx]
    assert_allclose(gv, gt, rtol=RTOL, atol=ATOL)

    arr_out = fbcorr(arr_in, arr_fb)
    gv = arr_out[idx]
    assert_allclose(gv, gt, rtol=RTOL, atol=ATOL)


def test_arr_out_3d():

    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    arr_out = np.zeros((20, 30, 8), dtype=DTYPE)

    arr_in[:] = np.arange(np.prod(arr_in.shape)).reshape(arr_in.shape)
    arr_fb[:] = np.arange(np.prod(arr_fb.shape)).reshape(arr_fb.shape)

    gt = np.array([[  1694.,   6198.,  10702.,  15206.,
                      19710.,  24214., 28718.,  33222.],
                   [  2462.,   9014.,  15566.,  22118.,
                      28670.,  35222., 41774.,  48326.]],
                  dtype=DTYPE)
    idx = [2, 3], [10, 12]

    fbcorr(arr_in, arr_fb, arr_out=arr_out)
    gv = arr_out[idx]
    assert_allclose(gv, gt, rtol=RTOL, atol=ATOL)

    arr_out = fbcorr(arr_in, arr_fb)
    gv = arr_out[idx]
    assert_allclose(gv, gt, rtol=RTOL, atol=ATOL)


def test_lena_npy_array():

    arr_in = lena()[::32, ::32].astype(DTYPE)
    arr_fb = np.empty((4, 3, 3), dtype=DTYPE)
    arr_fb[:] = np.arange(np.prod(arr_fb.shape)).reshape(arr_fb.shape)

    idx = [[4, 2], [4, 2]]

    gt = np.array(
        [[  5138.,  16667.,  28196.,  39725.],
         [  4232.,  13160.,  22088.,  31016.]],
        dtype=DTYPE)

    arr_out = fbcorr(arr_in, arr_fb)
    gv = arr_out[idx]
    assert_allclose(gv, gt, rtol=RTOL, atol=ATOL)


def test_lena_npy_array_float64():

    arr_in = lena()[::32, ::32].astype(np.float64)
    arr_fb = np.empty((4, 3, 3), dtype=np.float64)
    arr_fb[:] = np.arange(np.prod(arr_fb.shape)).reshape(arr_fb.shape)

    idx = [[4, 2], [4, 2]]

    gt = np.array(
        [[  5138.,  16667.,  28196.,  39725.],
         [  4232.,  13160.,  22088.,  31016.]],
        dtype=np.float64)

    arr_out = fbcorr(arr_in, arr_fb)
    gv = arr_out[idx]
    assert_allclose(gv, gt, rtol=RTOL, atol=ATOL)


def test_lena_npy_array_non_C_contiguous():

    arr_in = lena()[::32, ::32].astype(DTYPE)
    arr_in = np.asfortranarray(arr_in)
    arr_fb = np.empty((4, 3, 3), dtype=DTYPE)
    arr_fb[:] = np.arange(np.prod(arr_fb.shape)).reshape(arr_fb.shape)
    arr_fb = np.asfortranarray(arr_fb)

    idx = [[4, 2], [4, 2]]

    gt = np.array(
        [[  5138.,  16667.,  28196.,  39725.],
         [  4232.,  13160.,  22088.,  31016.]],
        dtype=DTYPE)

    arr_out = fbcorr(arr_in, arr_fb)
    gv = arr_out[idx]
    assert_allclose(gv, gt, rtol=RTOL, atol=ATOL)


def test_lena_pt3_array():

    lena32 = lena()[::32, ::32].astype(DTYPE) / 255.
    arr_in = np.empty(lena32.shape, dtype=DTYPE)
    arr_in[:] = lena32

    arr_fb = np.empty((4, 3, 3), dtype=DTYPE)
    arr_fb[:] = np.arange(np.prod(arr_fb.shape)).reshape(arr_fb.shape)

    idx = [[4, 2], [4, 2]]

    gt = np.array(
        [[  20.14902115,   65.36077881,  110.57255554,  155.78433228],
         [  16.59607887,   51.60784531,   86.61960602,  121.63137817]],
        dtype=DTYPE)

    arr_out = fbcorr(arr_in, arr_fb)
    gv = arr_out[idx]
    assert_allclose(gv, gt, rtol=RTOL, atol=ATOL)


# -----------------------------------------------------------------------------
# -- Test Errors
# -----------------------------------------------------------------------------

#@raises(AssertionError)
def test_error_arr_in_ndim():
    arr_in = np.zeros((1, 4, 4, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_error_arr_fb_ndim():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((3, 3, 4), dtype=DTYPE)
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_error_arr_fb_h_too_big():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 21, 1, 4), dtype=DTYPE)
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_error_arr_fb_h_even():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 2, 2, 4), dtype=DTYPE)
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_error_arr_fb_w_too_big():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 31, 4), dtype=DTYPE)
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_error_arr_fb_d_too_small():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 1), dtype=DTYPE)
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_error_arr_fb_dtype():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype='float64')
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_error_arr_out_h():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    arr_out = np.zeros((21, 30, 8), dtype=DTYPE)
    fbcorr(arr_in, arr_fb, arr_out=arr_out)

#@raises(AssertionError)
def test_error_arr_out_w():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    arr_out = np.zeros((20, 31, 8), dtype=DTYPE)
    fbcorr(arr_in, arr_fb, arr_out=arr_out)

#@raises(AssertionError)
def test_error_arr_out_d():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    arr_out = np.zeros((20, 30, 4), dtype=DTYPE)
    fbcorr(arr_in, arr_fb, arr_out=arr_out)

#@raises(AssertionError)
def test_error_arr_out_ndim():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    arr_out = np.zeros((4, 20, 30, 4), dtype=DTYPE)
    fbcorr(arr_in, arr_fb, arr_out=arr_out)

#@raises(AssertionError)
def test_error_arr_out_dtype():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    arr_out = np.zeros((20, 30, 8), dtype='float64')
    fbcorr(arr_in, arr_fb, arr_out=arr_out)

#@raises(AssertionError)
def test_arr_in_nan():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_in[4, 2] = np.nan
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_arr_in_inf():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_in[4, 2] = np.inf
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_arr_fb_nan():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    arr_in[4, 0] = np.nan
    fbcorr(arr_in, arr_fb)

#@raises(AssertionError)
def test_arr_fb_inf():
    arr_in = np.zeros((20, 30, 4), dtype=DTYPE)
    arr_fb = np.zeros((8, 1, 1, 4), dtype=DTYPE)
    arr_in[4, 0] = np.inf
    fbcorr(arr_in, arr_fb)
