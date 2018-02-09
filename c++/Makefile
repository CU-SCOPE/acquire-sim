

all: acquire


acquire: main.cpp v4ldevice.cpp
	$(CXX) -I /usr/local/include/opencv2 -Wall -g -O0 -o opencv-test main.cpp v4ldevice.cpp $(shell pkg-config --libs-only-l opencv libv4l2)

clean:
	$(RM) *.o
	$(RM) acquire
