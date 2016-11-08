import Furb
import skills

# setup
coco = Furb.Furb()

# register skills
sk=skills.all(coco)
coco.skills=sk

# set polling instruction


# run
coco.run()