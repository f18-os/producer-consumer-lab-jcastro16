# Producer Consumer Lab

Note: It's best to be run through an IDE as the program was constructed using PyCharm


# Purpose
Lab to be implemented through trivial producer-consumer system using
python threads where all coordination is managed the producers and
consumers. They will form a simple rendering pipeline using multiple threads. One
thread will read frames from a file, a second thread will take those frames
and convert them to grayscale, and the third thread will display those
frames. The threads will run concurrently.


## Using the Program
Run ExtractAndDisplay.py to see the magic happen. :)  

## File List
### ExtractFrames.py (Provided by Dr. Freudenthal)
Extracts a series of frames from the video contained in 'clip.mp4' and saves 
them as jpeg images in sequentially numbered files with the pattern
'frame_xxxx.jpg'.

### ConvertToGrayscale.py (Provided by Dr. Freudenthal)
Loads a series for frames from sequentially numbered files with the pattern
'frame_xxxx.jpg', converts the frames to grayscale, and saves them as jpeg
images with the file names 'grayscale_xxxx.jpg'

### DisplayFrames.py (Provided by Dr. Freudenthal)
Loads a series of frames sequently from files with the names
'grayscale_xxxx.jpg' and displays them with a 42ms delay.

### ExtractAndDisplay.py (Provided by Dr. Freudenthal, modifications were made)
Loads a series of frames from a video contained in 'clip.mp4' and displays them with a 42ms delay


## Requirements
* Extract frames from a video file, convert them to grayscale, and display
them in sequence
  * Can be observed when running ExtractAndDisplay.py
* You must have three functions
  * One function to extract the frames
	* function called "produce_frame" located under ExtractAndDisplay.py
  * One function to convert the frames to grayscale
	* function called "consume_frame" located under ExtractAndDisplay.py
  * One function to display the frames at the original framerate (24fps)
	* function called "display_frames" located under ExtractAndDisplay.py
* The functions must each execute within their own python thread
	* Every thread is defined under the ExtractAndDisplay.py 
  * The threads will execute concurrently - done
  * The order threads execute in may not be the same from run to run - done
	* In order to satisfy this requirement, my implementation consisted of
	running/playing the video as soon as there were at least two frames 
	processed. So the video doesn't play is the queue is empty. You can 
	see the implementation in code line #72.
* Threads will need to signal that they have completed their task
	* This was achieved by programming locks to identify when a frame 
	must be produced and when a frame must be consumed. What i mean by 
	this is the p_lock, c_lock and play_lock. The p_lock locks the 
	producer thread when the queue is full while at the same time 
	consumer unlocks when a frame is consumed. The p_lock is only
	there to be notified when two frames are available, the the video
	is to be played.   

	## Note: 
        * p_lock stops the producer from producing
	* c_lock stops the consumer from consuming 

* Threads must process all frames of the video exactly once
	* If run through the IDE, you can follow procedures on the console with
	print statements as to when frames are being produced, frames are
 	being consumed and frames being played. 
* Frames will be communicated between threads using producer/consumer idioms
  * Producer/consumer queues will be bounded at ten frames
	*See code line #164 on ExtractAndDisplay.py
