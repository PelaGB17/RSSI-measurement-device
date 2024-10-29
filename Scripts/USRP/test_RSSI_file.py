#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: test_RSSI_file
# GNU Radio version: 3.10.7.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time




class test_RSSI_file(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "test_RSSI_file", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.gain_rx = gain_rx = 40
        self.fm = fm = 100e3
        self.file = file = "f23_julio"
        self.fc = fc = 2.3e9
        self.distance = distance = 1

        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("serial=31BBEFE", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_0_0.set_center_freq(fc, 0)
        self.uhd_usrp_source_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0_0.set_gain(gain_rx, 0)
        self.uhd_usrp_source_0_0.set_auto_dc_offset(True, 0)
        self.uhd_usrp_source_0_0.set_auto_iq_balance(False, 0)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_float*1, (1, 1))
        self.blocks_skiphead_0_0 = blocks.skiphead(gr.sizeof_float*1, int(samp_rate))
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, int(samp_rate))
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(int(samp_rate), (1/samp_rate), 4000, 1)
        self.blocks_head_0 = blocks.head(gr.sizeof_float*1, 1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, file, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.band_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                (fm - 50e3),
                (fm + 50e3),
                100e3,
                window.WIN_HAMMING,
                6.76))
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, distance)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_skiphead_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_skiphead_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_skiphead_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.fm - 50e3), (self.fm + 50e3), 100e3, window.WIN_HAMMING, 6.76))
        self.blocks_moving_average_xx_0_0.set_length_and_scale(int(self.samp_rate), (1/self.samp_rate))
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)

    def get_gain_rx(self):
        return self.gain_rx

    def set_gain_rx(self, gain_rx):
        self.gain_rx = gain_rx
        self.uhd_usrp_source_0_0.set_gain(self.gain_rx, 0)

    def get_fm(self):
        return self.fm

    def set_fm(self, fm):
        self.fm = fm
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.fm - 50e3), (self.fm + 50e3), 100e3, window.WIN_HAMMING, 6.76))

    def get_file(self):
        return self.file

    def set_file(self, file):
        self.file = file
        self.blocks_file_sink_0.open(self.file)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.uhd_usrp_source_0_0.set_center_freq(self.fc, 0)

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance
        self.analog_const_source_x_0.set_offset(self.distance)




def main(top_block_cls=test_RSSI_file, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
