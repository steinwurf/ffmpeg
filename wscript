#! /usr/bin/env python
# encoding: utf-8

import os

APPNAME = 'ffmpeg'
VERSION = '1.1.0'


def configure(conf):

    conf.find_program('make')

    config_cmd = './configure --disable-programs --prefix={}'.format(
        conf.out_dir)

    conf.cmd_and_log(config_cmd,
                     cwd=str(conf.dependency_path('ffmpeg_source')))


def build(bld):

    ffmpeg_path = bld.dependency_path('ffmpeg_source')
    if bld.cmd == 'clean':
        bld.cmd_and_log('make clean', cwd=ffmpeg_path)
    else:
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

        include = os.path.join(bld.bldnode.abspath(), 'include')
        path = os.path.join(bld.bldnode.abspath(), 'lib')
        for lib in libs:
            bld.read_stlib(
                lib,
                paths=[path],
                export_includes=[include])


def distclean(ctx):
    ffmpeg_path = ctx.dependency_path('ffmpeg_source')
    ctx.cmd_and_log('make distclean', cwd=ffmpeg_path)
