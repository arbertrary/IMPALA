"""Parses plain text .srt subtitle files to XML"""
import re
import xml.etree.cElementTree as ET
from nltk import sent_tokenize, word_tokenize
from xml.dom import minidom


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
            lines = p.splitlines(keepends=False)

            if control_id != int(lines[0]):
                raise ValueError(lines[0])
            elif not re.fullmatch(time_pattern, lines[1].strip()):
                raise ValueError(lines[1])
            else:
                time = lines[1].split(" --> ")
                start = time[0].strip()
                end = time[1].strip()

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

    with open(dest_path, "w", encoding="UTF-8") as f:
        f.write(xmlstr)
