#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block

_syncword = '0010110111010100100101111111110111010011011110110000111100011111'

class smogp_signalling_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the SMOG-P signalling frames

    The input is a float stream of soft symbols. The output are PDUs
    with signalling frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "smogp_signalling_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(packlen = 64,\
                                           sync = _syncword,\
                                           threshold = syncword_threshold)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self, 'out'))

    _default_sync_threshold = 8
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds SMOG-P signalling deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
