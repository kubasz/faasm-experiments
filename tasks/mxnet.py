from os.path import join
from subprocess import run
from copy import copy
import os

from faasmcli.util.env import FAASM_TOOLCHAIN_FILE, SYSROOT_INSTALL_PREFIX
from faasmcli.util.files import clean_dir
from invoke import task

from tasks.util.env import EXPERIMENTS_THIRD_PARTY

MXNET_DIR = join(EXPERIMENTS_THIRD_PARTY, "mxnet")

# See the MXNet CPP guide for more info:
# https://mxnet.apache.org/versions/1.6/api/cpp


@task
def lib(ctx, clean=False):
    work_dir = join(MXNET_DIR, "build")

    clean_dir(work_dir, clean)

    env_vars = copy(os.environ)    

    cmake_cmd = [
        "cmake",
        "-DFAASM_BUILD_TYPE=wasm",
        "-DCMAKE_TOOLCHAIN_FILE={}".format(FAASM_TOOLCHAIN_FILE),
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_INSTALL_PREFIX={}".format(SYSROOT_INSTALL_PREFIX),
        "-DUSE_CUDA=OFF",
        "-DUSE_LAPACK=OFF",
        "-DUSE_MKL_IF_AVAILABLE=OFF",
        "-DUSE_F16C=OFF",
        "-DUSE_SSE=OFF",
        "-DUSE_OPENMP=OFF",
        "-DUSE_OPENCV=OFF",
        "-DUSE_INTGEMM=OFF",
        "-DUSE_OPERATOR_TUNING=OFF",
        "-DBUILD_CPP_EXAMPLES=OFF",
        "-DUSE_SIGNAL_HANDLER=OFF",
        "-DUSE_CCACHE=OFF",
        MXNET_DIR,
    ]

    cmake_str = " ".join(cmake_cmd)
    print(cmake_str)

    res = run(cmake_str, shell=True, cwd=work_dir, env=env_vars)
    if res.returncode != 0:
        raise RuntimeError("CMake command failed")

