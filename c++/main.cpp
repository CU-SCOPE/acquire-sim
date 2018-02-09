/*******************************************
 * Background Subtraction Algorithm for SCOPE
 * Author: Guy Margalit
 * 
 * Adapted from https://gist.github.com/TIS-Edgar/10f04501f49b6b3bf75e
*******************************************/

#include <iostream>
#include <sstream>
#include <stdio.h>
#include "v4ldevice.h"
#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>

using namespace cv;
using namespace std;

int main () {
    /*******************************************
     * Variables
    *******************************************/
    Mat frame; //current frame
    Mat fgMaskMOG2; //fg mask fg mask generated by MOG2 method
    Ptr<BackgroundSubtractor> pMOG2; //MOG2 Background subtractor
    IplImage* frameIpl;
    CvSize ImageSize;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;

    /*******************************************
     * Initialize Window
    *******************************************/
    unsigned char* ImageBuffer = NULL;
    int keyboard = -1;

    ImageSize.width = 640;
    ImageSize.height = 480;
    cv::namedWindow((char*)"Output", 1 );

    /*******************************************
     * Background Subtractor MOG2
    *******************************************/
    pMOG2 = createBackgroundSubtractorMOG2(); //MOG2 approach
    frameIpl = cvCreateImage(ImageSize , IPL_DEPTH_8U, 1 ); // Grayscale

    open_device((char*)"/dev/video0");
    init_device(ImageSize.width, ImageSize.height);
    start_capturing();

    while(keyboard == -1 )
    {
        ImageBuffer = snapFrame();
        if( ImageBuffer != NULL )
        {
            memcpy( frameIpl->imageData, ImageBuffer, frameIpl->imageSize);
            frame = cv::cvarrToMat(frameIpl);
            pMOG2->apply(frame, fgMaskMOG2);
            cv::findContours(fgMaskMOG2, contours, hierarchy,CV_RETR_EXTERNAL,CV_CHAIN_APPROX_SIMPLE, Point(0,0));      
            if(contours.size() > 0) {
				Scalar color = Scalar(0, 255, 0);
				drawContours(frame,contours,-1,color,2);
			}
            cv::imshow( (char*)"Output",frame);
            keyboard = cvWaitKey(10);
        }
        else
        {
            printf("No image buffer retrieved.\n");
            break;
        }
    }

    cvDestroyWindow( (char*)"Output" );
    stop_capturing();
    uninit_device();
    close_device();

    return 0;
}
