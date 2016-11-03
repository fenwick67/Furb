import Furb
import skills


coco = Furb.Furb()
sk=skills.all(coco)
coco.skills=sk
coco.run()