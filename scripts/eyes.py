import cv2
import mediapipe as mp
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness=1,circle_radius=1)
faces = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
eyes = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_eye.xml")
smiles = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_smile.xml")
eyesg = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_eye_tree_eyeglasses.xml")
catfaces = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalcatface.xml")
catfacese = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalcatface_extended.xml")
facealts = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_alt.xml")
facealt2s = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_alt2.xml")
facesat = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_alt_tree.xml")
fullbody = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_fullbody.xml")
le2s = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_lefteye_2splits.xml")
lpr16s = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_licence_plate_rus_16stages.xml")
lb = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_lowerbody.xml")
pf = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_profileface.xml")
re2s = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_righteye_2splits.xml")
rpn = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_russian_plate_number.xml")
ub = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_upperbody.xml")
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results = hands.process(imgRGB)
    resultsa = faceMesh.process(imgRGB)
    resultsf = faces.detectMultiScale(gray, 1.1, 19)
    resultss = smiles.detectMultiScale(gray, 1.4, 19)
    resultseg = eyesg.detectMultiScale(gray, 1.4, 19)
    results1 = catfaces.detectMultiScale(gray, 1.4, 19)
    results2 = catfacese.detectMultiScale(gray, 1.4, 19)
    results3 = facealts.detectMultiScale(gray, 1.4, 19)
    results4 = facealt2s.detectMultiScale(gray, 1.4, 19)
    results5 = facesat.detectMultiScale(gray, 1.4, 19)
    results6 = fullbody.detectMultiScale(gray, 1.4, 19)
    results7 = le2s.detectMultiScale(gray, 1.4, 19)
    results8 = lpr16s.detectMultiScale(gray, 1.4, 19)
    results9 = lb.detectMultiScale(gray, 1.4, 19)
    results10 = pf.detectMultiScale(gray, 1.4, 19)
    results11 = re2s.detectMultiScale(gray, 1.4, 19)
    results12 = rpn.detectMultiScale(gray, 1.4, 19)
    results13 = ub.detectMultiScale(gray, 1.4, 19)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    if resultsa.multi_face_landmarks:
        for faceLms in resultsa.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)
    if True == True:
        for (sx,sy,sw,sh) in resultss:
            cv2.rectangle(img, (sx,sy), (sx+sw,sy+sh), (0,0,255), 2)
            sentiment = 1
        else:
            sentiment = 0
    if True == True:
        for (yex,yey,yew,yeh) in resultseg:
            cv2.rectangle(img, (yex,yey), (yex+yew,yey+yeh), (100,100,100), 2)
    if True == True:
        for (x1,y1,w1,h1) in results1:
            cv2.rectangle(img, (x1,y1), (x1+w1,y1+h1), (100,0,155), 2)
    if True == True:
        for (x2,y2,w2,h2) in results2:
            cv2.rectangle(img, (x2,y2), (x2+w2,y2+h2), (223,0,155), 2)
    if True == True:
        for (x3,y3,w3,h3) in results3:
            cv2.rectangle(img, (x3,y3), (x3+w3,y3+h3), (123,12,155), 2)
    if True == True:
        for (x4,y4,w4,h4) in results4:
            cv2.rectangle(img, (x4,y4), (x4+w4,y4+h4), (12,0,155), 2)
    if True == True:
        for (x5,y5,w5,h5) in results5:
            cv2.rectangle(img, (x5,y5), (x5+w5,y5+h5), (100,0,155), 2)
    if True == True:
        for (x6,y6,w6,h6) in results6:
            cv2.rectangle(img, (x6,y6), (x6+w6,y6+h6), (223,0,155), 2)
    if True == True:
        for (x7,y7,w7,h7) in results7:
            cv2.rectangle(img, (x7,y7), (x7+w7,y7+h7), (123,12,155), 2)
    if True == True:
        for (x8,y8,w8,h8) in results8:
            cv2.rectangle(img, (x8,y8), (x8+w8,y8+h8), (12,0,155), 2)
    if True == True:
        for (x9,y9,w9,h9) in results9:
            cv2.rectangle(img, (x9,y9), (x9+w9,y9+h9), (121,0,155), 2)
    if True == True:
        for (x10,y10,w10,h10) in results10:
            cv2.rectangle(img, (x10,y10), (x10+w10,y10+h10), (111,0,155), 2)
    if True == True:
        for (x11,y11,w11,h11) in results11:
            cv2.rectangle(img, (x11,y11), (x11+w11,y11+h11), (2,0,153), 2)
    if True == True:
        for (x12,y12,w12,h12) in results12:
            cv2.rectangle(img, (x12,y12), (x12+w12,y12+h12), (123,123,2), 2)
    if True == True:
        for (x13,y13,w13,h13) in results13:
            cv2.rectangle(img, (x13,y13), (x13+w13,y13+h13), (123,132,132), 2)
    for (x,y,w,h) in resultsf:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        img_g_f = gray[y:y+h,x:x+w]
        resultse = eyes.detectMultiScale(img_g_f, 1.3, 19)
        for (ex,ey,ew,eh) in resultse:
            cv2.rectangle(img, (x+ex,y+ey), (x+ex+ew,y+ey+eh), (255,0,0), 2)
    cv2.imshow('Camera',img)
    cv2.waitKey(1)