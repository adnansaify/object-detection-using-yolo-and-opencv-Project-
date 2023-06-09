import numpy as np
import cv2

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []

with open("coco.names", "r") as file:
    classes = file.read().splitlines()

cap=cv2.VideoCapture('Sample.mp4')
#img=cv2.imread('download.jfif')

while True:
    _, img=cap.read()
    height, width, _=img.shape

    blob=cv2.dnn.blobFromImage(img, 1/255, (416,416), (0,0,0), swapRB=True, crop=False)
    #blob is to collect the image with some dimension and same depth which needd to be processed
    #swaprb is used to convert bgr image into lgb orders

    net.setInput(blob)

    output_layers_names=net.getUnconnectedOutLayersNames()
    layersoutputs=net.forward(output_layers_names)

    boxes=[]
    confidences=[]
    class_ids=[]

    for output in layersoutputs:
        for detection in output:
            scores=detection[5:]
            class_id=np.argmax(scores)
            confidence=scores[class_id]
            if confidence > 0.5:
                center_x=int(detection[0]*width)
                center_y = int(detection[1] * height)
                w=int(detection[2]*width)
                h=int(detection[3]*height)

                x=int(center_x-w/2)
                y=int(center_y-h/2)

                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    print(len(boxes))
    indexes=cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font=cv2.FONT_HERSHEY_PLAIN
    colors=np.random.uniform(0, 255, size=(len(boxes),3))

    for i in indexes.flatten():
        x,y,w,h =boxes[i]
        label=str(classes[class_ids[i]])
        confidence=str(round(confidences[i],2))
        color=colors[i]
        cv2.rectangle(img, (x,y), (x+w, y+h),color,2)
        cv2.putText(img,label + " " +confidence, (x,y+20), font,2,(255,255,255),2)

    cv2.imshow("Image", img)
    key=cv2.waitKey(1)
    if key==20:
        break

cap.release()
cv2.destroyAllWindows()
