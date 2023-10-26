
import json
import speech_recognition as sr  # type: ignore
from os import path, listdir
from typing import Dict, Literal
import ast
import spacy
import time


def get_audio_dict(type: Literal["clear", "other"]) -> Dict[str, str]:
    audo_files: Dict[str, str] = {}
    for speaker_id in listdir(f'audio_files/{type}'):
        speaker_path = path.join(path.dirname(path.realpath(__file__)),
                                 'audio_files', type, speaker_id)
        for chapter_id in listdir(speaker_path):
            chapter_path = path.join(speaker_path, chapter_id)
            with open(path.join(chapter_path, f"{speaker_id}-{chapter_id}.trans.txt"), 'r') as f:
                trans_file = f.readlines()
            for line in trans_file:
                audio_file_name, transcription = line.split(" ", 1)
                filepath = f"{path.join(chapter_path, audio_file_name)}.flac"
                audo_files[filepath] = transcription
    return audo_files


def sentece_similarity(sentece_1: str, setence_2: str):
    nlp = spacy.load("en_core_web_lg")
    return nlp(sentece_1).similarity(nlp(setence_2))


r = sr.Recognizer()

# score = 0
# audio_dict = get_audio_dict("clear").items()
# for file, trans in audio_dict:
#     with sr.AudioFile(file) as source:
#         audio = r.record(source)  # type: ignore
#     try:
#         ai_trans = str(r.recognize_sphinx(audio))  # type: ignore
#         if ai_trans.lower() == trans.lower():
#             score += 1
#             print(f"{score}/{len(audio_dict)}")
#         print(f"Expected: {trans.lower()}\nResult: {ai_trans.lower()}")
#     except sr.UnknownValueError:
#         print("Sphinx could not understand audio")
#     except sr.RequestError as e:
#         print("Sphinx error; {0}".format(e))
# print(f"{score}/{len(audio_dict)}")


score = 0
audio_dict = get_audio_dict("clear").items()
results = {}
try:
    for file, trans in audio_dict:
        if len(results) == 1000:
            break
        with sr.AudioFile(file) as source:
            audio = r.record(source)  # type: ignore
        try:
            results[file] = {}
            results[file]['trans'] = trans
            start_time = time.time()
            ai_trans = ast.literal_eval(r.recognize_vosk(audio))[  # type: ignore
                'text']
            execution_time = time.time() - start_time
            results[file]['ai_trans'] = ai_trans.lower()
            similarity = sentece_similarity(ai_trans.lower(), trans.lower())
            results[file]['similarity'] = similarity
            if similarity >= 0.9:
                score += 1
            print(
                f"{score}/{len(audio_dict)}\tSimilarity: {similarity}\tTime: {execution_time}")
            results[file]['with_error'] = False
        except sr.UnknownValueError:
            results[file]['with_error'] = True

finally:
    with open('result_vosk_clear_big.json_test', 'w') as fp:
        json.dump(results, fp)
    print(f"{score}/{len(audio_dict)}")
