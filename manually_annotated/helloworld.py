import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


orig = "scream_man_TODO.xml"
new = "scream.xml"

tree1 = ET.parse(orig)
tree2 = ET.parse(new)

for scene in tree1.findall("scene"):
    start = scene.get("start")
    end= scene.get("end")
    id1 = scene.get("id")

    if start:
        for s in tree2.findall("scene"):
            if id1 == s.get("id"):
                s.set("start", start)
                s.set("end", end)
            else:
                continue

    else:
        continue

tree2.write("scream_man.xml")

# path = "star-wars-4copy2.xml"
#
# tree = ET.parse(path)
# scenes = tree.findall("scene")
#
# beginning = datetime.strptime("00:00:00", '%H:%M:%S')
# current_start = datetime.strptime("00:00:00", '%H:%M:%S')
# current_end = datetime.strptime("00:00:00", '%H:%M:%S')
# start_time = 0
# end_time = 0
# for s in scenes:
#     scene_id = int(str(s.get("id")).replace("sc", ""))
#     if scene_id < 210:
#
#         continue
#     else:
#         if s.get("start") and s.get("end"):
#             print(scene_id)
#
#             current_start = datetime.strptime(s.get("start"), '%H:%M:%S')
#             current_end = datetime.strptime(s.get("end"), '%H:%M:%S')
#             start_time = (current_start-beginning).total_seconds()
#             end_time =(current_end-beginning).total_seconds()
#         else:
#             current_start += timedelta(seconds=2.5)
#             current_end += timedelta(seconds=2.5)
#
#             s.set("start", current_start.strftime('%H:%M:%S'))
#             s.set("end", current_end.strftime('%H:%M:%S'))
#
# tree.write("star-wars-4copy2.xml")


# def main():
#     print("Hello world!")
#
# if __name__ == '__main__':
#     main()
