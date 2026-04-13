class GestureDetector:
    def __init__(self, landmarks):
        self.landmarks=landmarks
    
    def fingers_up(self):
        if len(self.landmarks)<21:
            return [0,0,0,0,0]
        fingers=[]
        tip_ids=[8,12,16,20]
        if self.landmarks[4][1] > self.landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for tip in tip_ids:
            if self.landmarks[tip][2] < self.landmarks[tip-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    
    def distance(self, p1, p2):
        if len(self.landmarks)<21:
            return 0
        x1, y1=self.landmarks[p1][1], self.landmarks[p1][2]
        x2, y2= self.landmarks[p2][1], self.landmarks[p2][2]
        dist=((x1-x2)**2 + (y1-y2)**2)**0.5
        return dist
    
    
