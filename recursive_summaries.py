import os
import json
import openai
from time import time,sleep


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def get_next_chunk(filepath, name):
    numbers = filepath.replace('.txt','').replace(name,'')
    number = int(numbers) + 1
    if number < 10:
        filename = '%s000%s.txt' % (name, number)
    elif number < 100:
        filename = '%s00%s.txt' % (name, number)
    elif number < 1000:
        filename = '%s0%s.txt' % (name, number)
    return open_file('chunks/%s' % filename)


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    books = os.listdir('books/')
    for book in books:
        #recommended to do one book at a time.
        if 'looted' in book:
            continue
        if 'bonus' in book:
            continue
       # if 'sworn' in book:
       #     continue
        if 'entangled' in book:
            continue
        if 'hidden' in book:
            continue
        if 'reckless' in book:
            continue
        if 'forbidden' in book:
            continue
        if 'smoke' in book:
            continue
        name = book.replace('.txt', '')
        summaries = [i for i in os.listdir('summaries/') if name in i]
        outline = open_file('outlines/%s' % book)
        summary_chunk = ''
        for summary in summaries:
            #if prompt/completion is already done for this chunk, skip
            if os.path.isfile('prompts/%s' % summary):
                continue
            summary_chunk = summary_chunk + ' ' + open_file('summaries/%s' % summary)  # accumulate the summaries so far
            if len(summary_chunk) > 1500:  # if summary is too long, summarize
                print('summarizing the summaries...')
                prompt = open_file('prompt_summary.txt').replace('<<CHUNK>>', summary_chunk)
                prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
                summary_chunk = gpt3_completion(prompt)
            last_chunk = open_file('chunks/%s' % summary)  # get the chunk equal to the currently summarized one
            #this next step breaks when it looks for a chunk after the end of the book. needs a fix but not sure what
            #still works to generate content for fine tuning.
            try:
                next_chunk = get_next_chunk(summary, name)
            except FileNotFoundError:
                continue
            else:
                prompt = open_file('prompt_full.txt').replace('<<OUTLINE>>', outline).replace('<<SUMMARY>>', summary_chunk).replace('<<CHUNK>>', last_chunk)
                print(summary, len(prompt) + len(next_chunk))
                save_file(prompt, 'prompts/%s' % summary)
                save_file(next_chunk, 'completions/%s' % summary)