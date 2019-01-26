from ImageExample import ImageExample

f = open("learningExamples.txt","w+")
for i in range (1, 101):
    im = ImageExample("./photos/plastic/plastic"+str(i)+".jpg", "PLASTIC")
    st = im.getString()
    f.write(st + "\n")
for i in range (1, 101):
    im = ImageExample("./photos/paper/paper"+str(i)+".jpg", "PAPER")
    st = im.getString()
    f.write(st + "\n")
for i in range (1, 101):
    im = ImageExample("./photos/glass/glass"+str(i)+".jpg", "GLASS")
    st = im.getString()
    f.write(st + "\n")
f.close()