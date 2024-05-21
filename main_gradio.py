import gradio as gr

from _1_download_yt_video import download_video
from _2_extract_audio_from_yt_video import extract_audio
from _3_extract_text_from_audio import extract_text
from _4_summarize import summarize
from _utils import PARAMS_JSON_PATH, json_write

js = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';

    var text = 'YouTube Video Summarizer: Summarize youtube videos';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 100);
            }, i * 100);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""

def summarize_yt_video(
    yt_video_url,
    file_name,
    lang,
    word_limit,
    as_bullets
):
    # Create dictionary
    params_dict = {
        'YT_VIDEO_URL': f'{yt_video_url}',
        'FILE_NAME': f'{file_name}',
        'LANGUAGE': f'{lang}',
        'WORD_LIMIT': f'{word_limit}',
        'AS_BULLETS': f'{as_bullets}'
    }

    print(f'params_dict: {params_dict}')

    # We are saving params.json only for testing in a modular manner, the main gradio app doesn't need it
    json_write(PARAMS_JSON_PATH, params_dict)

    yt_video_url = params_dict['YT_VIDEO_URL']
    file_name = params_dict['FILE_NAME']
    lang = params_dict['LANGUAGE']
    word_limit = params_dict['WORD_LIMIT']
    as_bullets = eval(params_dict['AS_BULLETS'])

    downloaded_video_path = download_video(yt_video_url, file_name)
    extract_audio(file_name)
    transcription = extract_text(file_name, lang)
    (
        word_count,
        word_limit,
        summarized_text_1,
        summarized_text_2,
        summarized_text_path_1,
        summarized_text_path_2,
        transcribed_text_path
     ) = summarize(file_name, lang, word_limit, as_bullets)

    word_limit_message = f'Processing completed! The transcription has a word count of {word_count} which has been summarized within the word limit of {word_limit}. Please download the summarized text files as well as the transcription (if required).'
    return (
        gr.Video(value=downloaded_video_path),
        gr.Textbox(value=word_limit_message, visible=True),
        gr.Textbox(value=summarized_text_1, visible=True),
        gr.Textbox(value=summarized_text_2, visible=True),
        gr.Textbox(value=transcription, visible=True),
        gr.DownloadButton(value=summarized_text_path_1, visible=True, interactive=True),
        gr.DownloadButton(value=summarized_text_path_2, visible=True, interactive=True),
        gr.DownloadButton(value=transcribed_text_path, visible=True, interactive=True)
    )

def initiate_summarization(
    yt_video_url,
    file_name,
    lang,
    word_limit,
    as_bullets
):
    if(yt_video_url == '' or file_name == ''):
        raise gr.Error("Please enter a valid YouTube video URL and file name to continue")
    else:
        return summarize_yt_video(yt_video_url, file_name, lang, word_limit, as_bullets)


with gr.Blocks(
        title='Video Summarizer',
        # theme=gr.themes.Monochrome(), # Monochrome theme is good but js doesn't work with gr.themes.Monochrome()
        theme=gr.themes.Base(),
        # theme='gstaff/sketch',
        js=js,
        # head=head,
        # analytics_enabled=False,
        # fill_height=True
) as yt_summarizer:
    with gr.Row():
        with gr.Column():
            yt_video_url = gr.Textbox(label="Provide YT Video URL", info="Ideally source audio should be in English")
            file_name = gr.Textbox(label="Provide File Name")
            lang = gr.Radio(
                    label="Select Summary language",
                    choices=['English', 'Hindi', 'Spanish', 'French', 'German'],
                    # Verified that both mixtral and llama3 works well with the above five languages
                    value='English'
            )
            word_limit = gr.Slider(
                    50,
                    1000,
                    value=200,
                    step=50,
                    label="Select Word Limit",
                    info="Choose between 50 and 1000 | Ideally should be between 20% to 50% of the size of the original transcription"
            )
            as_bullets = gr.Checkbox(
                    label='Summarize as bullet points',
                    value=False
            )
            button = gr.Button("Summarize video", variant="primary", interactive=True, scale=1)
            word_limit_message = gr.Textbox(label="Word Limit", visible=False)
        with gr.Column():
            video_preview = gr.Video(label="YT Video Preview", width=640, height=480)

    with gr.Row():
        with gr.Column(variant='panel'):
            summarized_text_1 = gr.Textbox(label="Summary Version 1", lines=5, visible=False)
            download_button_1 = gr.DownloadButton(label="Download Summary Version 1", variant="primary", visible=False)
        with gr.Column(variant='panel'):
            summarized_text_2 = gr.Textbox(label="Summary Version 2", lines=5, visible=False)
            download_button_2 = gr.DownloadButton(label="Download Summary Version 2", variant="primary", visible=False)

    with gr.Row():
        with gr.Column(variant='panel'):
            original_text = gr.Textbox(label='Transcription', lines=7, visible=False)
            download_button_3 = gr.DownloadButton(label="Download Transcription", variant="primary", visible=False)

    button.click(
        fn=initiate_summarization,
        inputs=[
            yt_video_url,
            file_name,
            lang,
            word_limit,
            as_bullets
        ],
        outputs=[
            video_preview,
            word_limit_message,
            summarized_text_1,
            summarized_text_2,
            original_text,
            download_button_1,
            download_button_2,
            download_button_3
        ]
    )

yt_summarizer.queue(api_open=False, default_concurrency_limit=5).launch(server_port=7862)  # Local launch
