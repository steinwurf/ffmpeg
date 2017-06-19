#! /usr/bin/env python
# encoding: utf-8

import os
import waflib
import waflib.Tools.ccroot

APPNAME = 'ffmpeg'
VERSION = '1.0.0'


def configure(conf):
    conf.find_program('make')


def build(bld):

    path = os.path.join(bld.bldnode.abspath(), 'build.log')
    bld.logger = waflib.Logs.make_logger(path, 'cfg')
    ffmpeg_path = bld.dependency_path('ffmpeg')

    config_cmd = './configure --disable-programs --prefix={}'.format(
        bld.bldnode.abspath())

    bld.cmd_and_log(config_cmd, cwd=ffmpeg_path)
    bld.cmd_and_log('make -j {}'.format(bld.options.jobs), cwd=ffmpeg_path)
    bld.cmd_and_log('make install', cwd=ffmpeg_path)

    libs = [
        'avcodec',
        'avdevice',
        'avfilter',
        'avformat',
        'avutil',
        'swresample',
        'swscale']

    for lib in libs:
        waflib.Tools.ccroot.read_stlib(
            bld,
            lib,
            paths=['./build/lib'],
            export_includes=['./build/include'])
