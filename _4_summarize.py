import os
from groq import Groq
from _utils import OUTPUT_DIR, write_text_file, read_text_file, PARAMS_JSON_PATH, json_read


def summarize(file_name, word_limit, as_bullets, transcribed_text=None):
    print("Initiating text summarization of the extracted text")
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        # Currently it supports only three models - gemma(bad), llama3-70b, and mixtral-8x7b
        # Need to update this if groq withdraws any of the three above llm (e.g. it has stopped hosting llama2)
    )

    transcribed_text_path = f'{OUTPUT_DIR}/{file_name}_orig.txt'
    if transcribed_text == None:
        text = read_text_file(transcribed_text_path)
    word_count = len(text.split()) # Counts the number of words while len(text) counts the number of characters

    calc_word_limit = False
    if word_limit == "0":
        print('No word limit entered by the user, using default word_limit')
        calc_word_limit = True
    elif int(word_limit) >= word_count:
        print('Word limit cannot exceed word count')
        calc_word_limit = True
    elif int(word_limit) > int(word_count * 0.75):
        print('Word limit must be atmost 75% of word count')
        calc_word_limit = True

    if calc_word_limit == True: # This could be changed as required
        print('Input word limit is not valid so, calculating word limit based on word count')
        if word_count >= 3500:
            print('Word limit exceeded. Aborting!!')
            return
        elif word_count >= 1000:
            word_limit = 250
        elif word_count >= 500:
            word_limit = 200
        elif word_count >= 250:
            word_limit = int(word_count*0.5)
        elif word_count >= 100:
            word_limit = int(word_count*0.75)
        elif word_count >=0:
            word_limit = word_count


    # prompt = (f'Summarize the text below of {word_count} words within the hard word limit of {word_limit} words '
    #           f'in {lang} language ')
    #
    # suffix = f'{word_limit}w_{lang.lower()[:3]}'

    prompt = f'Summarize the text below of {word_count} words within the hard word limit of {word_limit} words '
    suffix = f'{word_limit}w'

    if as_bullets == True:
        print('Summarization sytle is as bullets')
        prompt += 'as bullet points. '
        suffix += '_as_bul'

    else:
        print('Summarization sytle is as paragraphs')
        prompt += 'as paragraphs. '

    prompt += 'Begin the summary by saying that this youtube video is about: '
    print(f'Prompt = {prompt}')
    text = prompt + text
    print(f'Word count of {word_count} would be summarized within the word limit of {word_limit}')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path_mixtral = f'{OUTPUT_DIR}/{file_name}_{suffix}_mixtral.txt'
    output_path_llama3_70b = f'{OUTPUT_DIR}/{file_name}_{suffix}_llama3_70b.txt'

    # mixtral supports hindi
    chat_completion_mixtral = client.chat.completions.create( # Works upto a token size of 32768
        messages=[
            {
                "role": "user",
                "content": text
            }
        ],
        model="mixtral-8x7b-32768"
    )

    # Best open source model yet | # Verified that lLama3 supports hindi
    chat_completion_llama3_70b = client.chat.completions.create(  # Works only when the token size is limited to 4096
        messages=[
            {
                "role": "user",
                "content": text
            }
        ],
        model="llama-3.1-70b-Versatile"
    )

    # # gemma-7b-it doesn't support hindi
    # # also, gemma is just bad
    # chat_completion_gemma_7b = client.chat.completions.create(  # Works only when the token size is limited to 8092
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": text,
    #         }
    #     ],
    #     model="gemma-7b-it"
    # )

    summary_mixtral = chat_completion_mixtral.choices[0].message.content
    summary_llama3_70b = chat_completion_llama3_70b.choices[0].message.content
    # summary_gemma_7b = chat_completion_gemma_7b.choices[0].message.content

    write_text_file(output_path_mixtral, summary_mixtral)
    write_text_file(output_path_llama3_70b, summary_llama3_70b)
    # write_text_file(output_path_gemma_7b, summary_gemma_7b)

    print("Text summarization complete")
    return (
        word_count,
        word_limit,
        summary_mixtral,
        summary_llama3_70b,
        output_path_mixtral,
        output_path_llama3_70b,
        transcribed_text_path
    )

if __name__ == "__main__": # Commented out as using gradio app instead of running step wise | May need debugging
    params_dict = json_read(PARAMS_JSON_PATH)
    file_name = params_dict['FILE_NAME']
    word_limit = params_dict['WORD_LIMIT']
    as_bullets = eval(params_dict['AS_BULLETS'])
    summarize(file_name, word_limit, as_bullets)