import torch
import whisper

from _utils import (AUDIO_DIR, JSON_DIR, OUTPUT_DIR, PARAMS_JSON_PATH, LANG_CODE_DICT, json_read, json_write, write_text_file)


def base_model_transcribe(lang, audio_path):
    base_model = 'medium' # Using medium as large gives CUDA OOM error
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using model: {base_model} on device: {device}')
    model = whisper.load_model(base_model, device=device, in_memory=True)
    # lang_code = LANG_CODE_DICT[lang]

    return model.transcribe(
        audio_path,
        language='en',
        task='translate',  # Using translate instead of transcribe as it works slightly better
        # task='transcribe',
        # word_timestamps=True
    )


def extract_text(file_name, lang):

    audio_file = f'{file_name}.wav'
    audio_path = f'{AUDIO_DIR}/{audio_file}'

    print(f'Processing audio file: {audio_file} and extracting text in {lang} language')

    """ 
    Languages supported by Whisper:
    Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, 
    Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, 
    Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, 
    Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, 
    Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.
    """

    result = base_model_transcribe(lang, audio_path)
    text = result['text']
    suffix_1 = f'orig'

    original_text_path = f'{OUTPUT_DIR}/{file_name}_{suffix_1}.txt'
    write_text_file(original_text_path, text)

    print(f'Generated text as .json for {audio_file} and saved it at {JSON_DIR}')
    return text

if __name__ == "__main__": # Commented out as using gradio app instead of running step wise | May need debugging
    params_dict = json_read(PARAMS_JSON_PATH)
    file_name = params_dict['FILE_NAME']
    lang = params_dict['LANGUAGE']
    extract_text(file_name, lang)

