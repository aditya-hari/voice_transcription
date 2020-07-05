from deepspeech import Model
import spacy
import numpy as np

def get_text(fin):
    asr = Model('models/final_model.pbmm')
    asr.enableExternalScorer('models/lm.scorer')
    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
    
    return asr.stt(audio)

def get_entities(text):
    nlp = spacy.load("en_ner_bc5cdr_md")
    doc = nlp(text)
    ents = doc.ents
    sym = []
    drg = []
    for i in ents:
        if i.label_ == 'DISEASE':
            sym.append(i)
        else:
            drg.append(i)
    return {'transcript':text, 'symptoms':sym, 'drugs':drg}
