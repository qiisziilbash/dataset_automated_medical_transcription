# %%
import os
import re
from typing import Dict, List, Tuple
import unidecode


source_dir = "transcripts/source_text"


def process_talk_turn(text: str) -> Dict[str, str]:
    if "\n" not in text:
        return text

    # Replace "-\n" with empty string and standalone "\n" with space
    processed_text = text.replace("-\n", "").replace("\n", " ")
    processed_text = unidecode.unidecode(processed_text)
    return processed_text


def parse_txt_d0420_s1(filename: str) -> Dict[str, str]:
    def extract_segments(text: str) -> List[str]:
        pattern = r"(?:Clinician:|Patient:)(.*?)(?=(?:Clinician:|Patient:)|$)"
        matches = re.findall(pattern, text, re.DOTALL)
        return [match.strip() for match in matches]

    def extract_speaker_code(text: str) -> Tuple[str, str]:
        pattern = r"^\((.*?)\)"
        matches = re.findall(pattern, text)
        if len(matches):
            return matches[0][-1], text[text.find(")") + 1 :].strip()
        else:
            raise ValueError(f"Expected a speaker code at start of text: {text}")

    data = []
    with open(filename, "r") as file:
        text = file.read()

        for talk_turn in extract_segments(text):
            speaker, content = extract_speaker_code(talk_turn)
            data.append({"speaker": speaker, "content": process_talk_turn(content)})

    return data


def parse_txt(filename: str) -> str:
    def extract_segments(text: str) -> List[str]:
        pattern = r"((?:THERAPIST:|CLIENT:).*?)(?=(?:THERAPIST:|CLIENT:)|$)"
        matches = re.findall(pattern, text, re.DOTALL)
        return [match.strip() for match in matches]

    data = []
    with open(filename, "r") as file:
        text = file.read()
        text = text[text.find("BEGIN TRANSCRIPT:") + len("BEGIN TRANSCRIPT:") : text.find("END TRANSCRIPT")]
        for talk_turn in extract_segments(text):
            speaker = "A" if talk_turn[: talk_turn.find(":")].strip() == "THERAPIST" else "B"
            content = process_talk_turn(talk_turn[talk_turn.find(":") + 1 :].strip())
            data.append({"speaker": speaker, "content": process_talk_turn(content)})
    return data


# %%
data = {}
for filename in os.listdir(source_dir):
    if filename.startswith("D0420-S1"):
        data[filename.replace(".txt", "")] = parse_txt_d0420_s1(os.path.join(source_dir, filename))
    else:
        data[filename.replace(".txt", "")] = parse_txt(os.path.join(source_dir, filename))


# %%
