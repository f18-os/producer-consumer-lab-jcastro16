#!/usr/bin/env python3
from threading import Event
import threading

import cv2
import numpy as np
import base64
import queue


play_lock = Event()
producer_finished_lock = Event()


class ProducerThread(threading.Thread):
    def __init__(self, name, fileName, c_lock, p_lock, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.fileName = fileName
        self.c_lock = c_lock
        self.p_lock = p_lock
        self.queue = queue

    def run(self):
        print("Starting " + self.name)
        produce_frame(self.fileName, self.c_lock, self.p_lock, self.queue)
        print("Exiting " + self.name)


class ConsumerThread(threading.Thread):
    def __init__(self, name,  c_lock, p_lock, queue, buffer):
        threading.Thread.__init__(self)
        self.name = name
        self.c_lock = c_lock
        self.p_lock = p_lock
        self.queue = queue
        self.buffer = buffer

    def run(self):
        print("Starting " + self.name)
        consume_frame(self.c_lock, self.p_lock, self.queue, self.buffer)
        print("Exiting " + self.name)





# Converts frames from queue to grayscale
def consume_frame(c_lock, p_lock, pc_queue, output_buffer):
    # Initialize frame count
    count = 0
    while 1:
        if producer_finished_lock.isSet() and pc_queue.empty():
            return

        if not pc_queue.empty():
            gray_scale_frame = cv2.cvtColor(pc_queue.get(), cv2.COLOR_BGR2GRAY)
            # get a jpg encoded frame
            success, jpgImage = cv2.imencode('.jpg', gray_scale_frame)

            # encode the frame as base 64 to make debugging easier
            jpgAsText = base64.b64encode(jpgImage)

            output_buffer.put(jpgAsText)
            print("                   Consumed Frame {}".format(count))

            if not p_lock.isSet():
                print("Unlocking P")
                p_lock.set()
            count += 1

            # Play if there is at least 2 frames to display
            if not play_lock.isSet() and count > 1:
                play_lock.set()
        else:
            print("                   Locking C (queue empty)")
            c_lock.wait()


# Extract frames and adds to queue
def produce_frame(file_name, c_lock, p_lock, pc_queue):
    # Initialize frame count 
    count = 0
    p_lock.set()

    # open video file
    vidcap = cv2.VideoCapture(file_name)

    # read first image
    success,image = vidcap.read()
    
    while success:
        if not pc_queue.full():
            # add the frame to the queue
            pc_queue.put(image)
            print("Produced Frame {}".format(count))

            if not c_lock.isSet():
                print("                   Unlocking C")
                c_lock.set()
        else:
            print("Locking P (queue full)")
            p_lock.wait()
            pc_queue.put(image)
            pass
       
        success,image = vidcap.read()
        count += 1

    print("Frame extraction complete")
    producer_finished_lock.set()




# Display frames at original frame rate
def display_frames(frames, lock):
    lock.wait()
    print("------------------------------------------ display frames started");
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    while not frames.empty():
        # get the next frame
        frameAsText = frames.get()

        # decode the frame
        jpgRawImage = base64.b64decode(frameAsText)

        # convert the raw frame to a numpy array
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)

        # get a jpg encoded frame
        img = cv2.imdecode(jpgImage, cv2.IMREAD_UNCHANGED)

        print("------------------------------------------ Displaying frame {}".format(count))

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()


# filename of clip to load
filename = 'clip.mp4'

# video frames queue
#video_queue_normal = queue.Queue()
video_queue_gray = queue.Queue()

# locks
c_lock = Event() # Used to lock consumer thread
p_lock = Event() # Used to lock producer thread

# Producer/Consumer shared queue
pc_queue = queue.Queue(10)

# extract the frames
producerThread = ProducerThread("Producer Thread", filename, c_lock, p_lock, pc_queue)
producerThread.start()

consumerThread = ConsumerThread("Consumer Thread", c_lock, p_lock, pc_queue, video_queue_gray)
consumerThread.start()

display_frames(video_queue_gray,play_lock)