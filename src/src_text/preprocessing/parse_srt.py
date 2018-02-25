import os
import re
import xml.etree.cElementTree as ET
from typing import List, Tuple
from nltk import sent_tokenize, word_tokenize
from xml.dom import minidom

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def srt_to_xml(srt_path: str, dest_path: str):
    """Parses subtitles from .srt plain text format to xml"""

    root = ET.Element("document")

    with open(srt_path) as file:
        text = file.read().strip()
        text = re.sub(r"<.{1,2}>", "", text)

        paragraphs = text.split("\n\n")
        time_pattern = re.compile(r"\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d")

        s_id = 1
        time_id = 1
        control_id = 1

        for p in paragraphs:
            # p = paragraphs[12]
            lines = p.splitlines(keepends=False)

            if control_id != int(lines[0]):
                raise ValueError(lines[0])
            elif not re.fullmatch(time_pattern, lines[1].strip()):
                raise ValueError(lines[1])
            else:
                time = lines[1].split(" --> ")
                start = time[0].strip()
                end = time[1].strip()


                # print(start)
                # print(end)

                dialogue = sent_tokenize(" ".join(lines[2:]))
                for sentence in dialogue:
                    start_id = "T" + str(time_id) + "S"
                    end_id = "T" + str(time_id) + "E"
                    w_id = 1
                    s = ET.SubElement(root, "s", id=str(s_id))
                    ET.SubElement(s, "time", id=start_id, value=start)

                    for w in word_tokenize(sentence):
                        word_id = str(s_id) + "." + str(w_id)
                        w_id += 1
                        ET.SubElement(s, "w", id=word_id).text = w

                    ET.SubElement(s, "time", id=end_id, value=end)
                    s_id += 1
                    time_id += 1
            control_id += 1

    tree = ET.ElementTree(root)
    xmlstr = minidom.parseString(ET.tostring(tree.getroot())).toprettyxml(indent="   ")
    # print(xmlstr)

    with open(dest_path, "w", encoding="UTF-8") as f:
        f.write(xmlstr)



def edit_opus_xml(xml_path: str):
    tree = ET.parse(xml_path)

    sentences = tree.findall("s")

    current_start = ""
    current_end = ""


    for s in sentences:
        s_id = s.get("id")
        start_id = "T"+s_id+"S"
        end_id = "T"+s_id+"E"

        times = s.findall("time")
        if len(times) == 2:
            print(times[0].get("id"))
            times[0].set("id", start_id)

            times[1].set("id", end_id)
            current_start = times[0].get("value")
        elif len(times) == 1 and times[0].get("id").endswith("S"):
            times[0].set("id", start_id)
            current_start = times[0].get("value")
        elif len(times) == 1 and times[0].get("id").endswith("E"):
            times[0].set("id", end_id)
            start = ET.Element("time", {"id": start_id, "value": current_start})
            s.insert(0, start)
        else:
            start = ET.Element("time", {"id": start_id, "value": current_start})
            s.insert(0, start)

    # sentences = tree.findall("s")
    # for s in reversed(sentences):
    #     s_id = s.get("id")
    #     start_id = "T" + s_id + "S"
    #     end_id = "T" + s_id + "E"
    #
    #     times = s.findall("time")
    #
    #     if len(times) == 2:
    #         # times[0].set("id", start_id)
    #         # times[1].set("id", end_id)
    #         # current_start = times[0].get("value")
    #         current_end = times[1].get("value")
    #         continue
    #
    #     elif len(times) == 1 and times[0].get("id").endswith("S"):
    #         times[0].set("id", start_id)
    #         end = ET.Element("time", {"id": end_id, "value": current_end})
    #         print("test")
    #
    #         s.insert(len(list(s)),end)
    #     elif len(times) == 1 and times[0].get("id").endswith("E"):
    #         times[0].set("id", end_id)
    #         current_end = times[0].get("value")
    #     else:
    #         end = ET.Element("time", {"id": end_id, "value": current_end})
    #         s.insert(len(list(s)),end)

    tree.write("test.xml")


def main():
    """main"""
    dir = os.path.join(BASE_DIR, "src/testfiles")
    path = os.path.join(BASE_DIR, "src/testfiles/", "star-wars-4_subs.xml")
    # edit_opus_xml(path)
    edit_opus_xml(path)


if __name__ == '__main__':
    main()
