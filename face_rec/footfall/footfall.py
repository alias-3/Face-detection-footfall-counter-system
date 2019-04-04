# import the necessary packages
from .pyimagesearch.centroidtracker import CentroidTracker
from .pyimagesearch.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib
import datetime
import cv2
import os
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()

# #Optional input 
# ap.add_argument("-i", "--input", type=str,
# 	help="path to optional input video file")

# ap.add_argument("-c", "--confidence", type=float, default=0.4,
# 	help="minimum probability to filter weak detections")

# ap.add_argument("-s", "--skip-frames", type=int, default=30,
# 	help="# of skip frames between detections")

# args = vars(ap.parse_args())
def count():
	input1="face_rec/footfall/videos/xyz.mp4"

	#Required models import

	prototxt_model=os.path.join(os.getcwd(),"face_rec\\footfall\\mobilenet_ssd\\MobileNetSSD_deploy.prototxt")
	caffe_model=os.path.join(os.getcwd(),"face_rec\\footfall\\mobilenet_ssd\\MobileNetSSD_deploy.caffemodel")

	#Output is stored at the directory output/output_current time
	output1="face_rec/footfall/output/output_{}.avi".format(datetime.datetime.now().timestamp())


	#Initialize the list of class labels MobileNet SSD was trained total detect

	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]

	#Load our serialized models from disk
	print("Loading...")

	net = cv2.dnn.readNetFromCaffe(prototxt_model, caffe_model)

	#If a video path was not supplied, grab a reference to the webcam
	if not input1:
		print("Starting video Camera...")
		vs = VideoStream(src=0).start()
		time.sleep(2.0)

	#Otherwise,go to the video file
	else:
		print("Opening video file...")
		vs = cv2.VideoCapture(input1)
		

	#Initialize the video writer
	writer = None

	#Initialize the frame dimensions 
	W = None
	H = None

	#Instantiate centroid tracker, then initialize a list to store our dlib correlation trackers, followed by a dictionary to
	#map each unique object ID to a TrackableObject

	ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
	trackers = []
	trackableObjects = {}

	# initialize the total number of frames processed thus far, along
	# with the total number of objects that have moved either up or down
	totalFrames = 0
	totalDown = 0
	totalUp = 0

	# start the frames per second throughput estimator
	# fps = FPS().start()

	# loop over frames from the video stream
	while True:
		# grab the next frame and handle if we are reading from either
		# VideoCapture or VideoStream
		frame = vs.read()
		
		frame = frame[1] if input1 else frame

		# if we are viewing a video and we did not grab a frame then we
		# have reached the end of the video
		if input1 is not None and frame is None:
			break

		# resize the frame to have a maximum width of 500 pixels (the
		# less data we have, the faster we can process it, then convert
		# the frame from BGR to RGB for dlib
		frame = imutils.resize(frame, width=500)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# if the frame dimensions are empty, set them
		if W is None or H is None:
			(H, W) = frame.shape[:2]

		# if we are supposed to be writing a video to disk, initialize
		# the writer
		if output1 is not None and writer is None:
			fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			writer = cv2.VideoWriter(output1, fourcc, 30,
				(W, H), True)

		rects = []

		if totalFrames % 30 == 0:
			# set the status and initialize our new set of object trackers
			trackers = []

			# convert the frame to a blob and pass the blob through the
			# network and obtain the detections
			blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
			net.setInput(blob)
			detections = net.forward()

			# Loop over the detections
			for i in np.arange(0, detections.shape[2]):
				# extract the confidence (i.e., probability) associated
				# with the prediction
				confidence = detections[0, 0, i, 2]

				# filter out weak detections by requiring a minimum
				# confidence
				if confidence > 0.4:
					# extract the index of the class label from the
					# detections list
					idx = int(detections[0, 0, i, 1])

					# if the class label is not a person, ignore it
					if CLASSES[idx] != "person":
						continue

					# compute the (x, y)-coordinates of the bounding box
					# for the object
					box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
					(startX, startY, endX, endY) = box.astype("int")

					# construct a dlib rectangle object from the bounding
					# box coordinates and then start the dlib correlation
					# tracker
					tracker = dlib.correlation_tracker()
					rect = dlib.rectangle(int(startX), int(startY), int(endX), int(endY))
					tracker.start_track(rgb, rect)

					# add the tracker to our list of trackers so we can
					# utilize it during skip frames
					trackers.append(tracker)
		else:
			# loop over the trackers
			for tracker in trackers:
				# update the tracker and grab the updated position
				tracker.update(rgb)
				pos = tracker.get_position()

				# unpack the position object
				startX = int(pos.left())
				startY = int(pos.top())
				endX = int(pos.right())
				endY = int(pos.bottom())

				# add the bounding box coordinates to the rectangles list
				rects.append((startX, startY, endX, endY))

		# draw a horizontal line in the center of the frame -- once an
		# object crosses this line we will determine whether they were
		# moving 'up' or 'down'
		# cv2.line(frame, (0, H // 2), (W, H // 2), (0, 255, 255), 2)

		# use the centroid tracker to associate the (1) old object
		# centroids with (2) the newly computed object centroids
		objects = ct.update(rects)

		# loop over the tracked objects
		for (objectID, centroid) in objects.items():
			# check to see if a trackable object exists for the current
			# object ID
			to = trackableObjects.get(objectID, None)

			# if there is no existing trackable object, create one
			if to is None:
				to = TrackableObject(objectID, centroid)

			# otherwise, there is a trackable object so we can utilize it
			# to determine direction
			else:
				# the difference between the y-coordinate of the *current*
				# centroid and the mean of *previous* centroids will tell
				# us in which direction the object is moving (negative for
				# 'up' and positive for 'down')
				y = [c[1] for c in to.centroids]
				direction = centroid[1] - np.mean(y)
				to.centroids.append(centroid)

				# check to see if the object has been counted or not
				if not to.counted:
					# if the direction is negative (indicating the object
					# is moving up) AND the centroid is above the center
					# line, count the object
					if direction < 0 and centroid[1] < H // 2:
						totalUp += 1
						to.counted = True

					# if the direction is positive (indicating the object
					# is moving down) AND the centroid is below the
					# center line, count the object
					elif direction > 0 and centroid[1] > H // 2:
						totalDown += 1
						to.counted = True

			# store the trackable object in our dictionary
			trackableObjects[objectID] = to

		# construct a tuple of information we will be displaying on the
		# frame
		info = [
			("Exit", totalUp),
			("Entered", totalDown),
		]

		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{} - {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 25) + H-50)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

		# check to see if we should write the frame to disk
		if writer is not None:
			writer.write(frame)

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		# increment the total number of frames processed thus far and
		# then update the FPS counter
		totalFrames += 1
		# fps.update()

	# stop the timer and display FPS information
	# fps.stop()
	# print("Elapsed time: {:.2f}".format(fps.elapsed()))
	# print("Approx. FPS: {:.2f}".format(fps.fps()))

	# check to see if we need to release the video writer pointer
	if writer is not None:
		writer.release()

	# if we are not using a video file, stop the camera video stream
	if not input1:
		vs.stop()

	# otherwise, release the video file pointer
	else:
		vs.release()

	# close any open windows
	cv2.destroyAllWindows()