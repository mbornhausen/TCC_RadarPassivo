import numpy as np
import csv
import time
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Save FFT to CSV',
            in_sig=[(np.float32, 32768)],
            out_sig=[]
        )
        self.filename = "fft_magnitude.csv"
        self.start_time = time.time()
        self.header_written = False

    def work(self, input_items, output_items):
        fft_vectors = input_items[0]  # shape: (N, 32768)

        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)

            if not self.header_written:
                # Write header: tempo, mag0, mag1, ..., mag32767
                header = ['timestamp'] + [f'mag_{i}' for i in range(32768)]
                writer.writerow(header)
                self.header_written = True

            for vector in fft_vectors:
                timestamp = time.time() - self.start_time
                row = [timestamp] + vector.tolist()
                writer.writerow(row)

        return len(input_items[0])
