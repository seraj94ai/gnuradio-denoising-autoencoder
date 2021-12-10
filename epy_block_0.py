# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 10:38:16 2021

@author: seraj
"""

"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from tensorflow.keras.models import load_model

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='denoising',   # will show up in GRC
            in_sig=[(np.float32,1024)],
            out_sig=[(np.float32,1024)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.autoencoder = load_model(r'C:\Users\seraj\Desktop\denoise\denoising.h5')

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        print("input_items",np.shape(np.array(input_items[0][0])))
        noisy_sig = input_items[0][0]
        de_noising_sig = self.autoencoder.predict(np.array([noisy_sig])/255.)*255
        print("de_noising_sig",np.shape(np.array(de_noising_sig)))
        for i in range(1,len(output_items[0])):
            output_items[0][i][:] = de_noising_sig
        print("output_items",np.shape(np.array(output_items[0][0])))	
        return len(output_items[0])
