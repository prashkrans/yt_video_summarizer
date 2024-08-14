import torch
import whisper

from _utils import (AUDIO_DIR, JSON_DIR, OUTPUT_DIR, PARAMS_JSON_PATH, json_read, write_text_file)


def base_model_transcribe(audio_file_path, to_eng):
    # base_model = 'medium'
    base_model = 'large-v2'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using model: {base_model} on device: {device}')
    model = whisper.load_model(base_model, device=device, in_memory=True)
    if to_eng:
        task = "translate"
    else:
        task = "transcribe"

    result = model.transcribe(
        audio_file_path,
        task=task,
        # word_timestamps=True
    )

    return result['text']


def transcribe(file_name, to_eng):
    audio_file = f'{file_name}.wav'
    audio_file_path = f'{AUDIO_DIR}/{audio_file}'

    print(f'Processing audio file: {audio_file} and extracting text')
    print(f'Processing audio file: {audio_file_path}')

    """ 
    TRANSLATE_TO_ENGLISHs supported by Whisper:
    Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, 
    Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, 
    Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, 
    Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, 
    Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.
    """

    transcribed_text = base_model_transcribe(audio_file_path, to_eng)
    suffix_1 = f'orig'

    original_text_path = f'{OUTPUT_DIR}/{file_name}_{suffix_1}.txt'
    write_text_file(original_text_path, transcribed_text)

    print(f'Generated text as .json for {audio_file} and saved it at {JSON_DIR}')
    return transcribed_text

if __name__ == "__main__": # Commented out as using gradio app instead of running step wise | May need debugging
    params_dict = json_read(PARAMS_JSON_PATH)
    file_name = params_dict['FILE_NAME']
    to_eng = eval(params_dict['TRANSLATE_TO_ENGLISH'])
    transcribe(file_name, to_eng)

