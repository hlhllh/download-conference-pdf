import argparse
import json
import os
from collections import defaultdict
from tqdm import tqdm
import openreview
import re

# client = openreview.Client(baseurl='https://api.openreview.net', username='<your username>', password='<your password>')
# notes = openreview.tools.iterget_notes(client, invitation='ICLR.cc/2019/Conference/-/Blind_Submission')
# for note in notes:
#     print(note.content['title'])


def download_iclr19(client, outdir='./rl/', get_pdfs=False):
    '''
    Main function for downloading ICLR metadata (and optionally, PDFs)
    '''
    # pylint: disable=too-many-locals

    print('getting metadata...')
    # get all ICLR '19 submissions, reviews, and meta reviews, and organize them by forum ID
    # (a unique identifier for each paper; as in "discussion forum").
    submissions = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2021/Conference/-/Blind_Submission')
    submissions_by_forum = {n.forum: n for n in submissions}
    # submissions_by_titile = {n.content['title']: n for n in submissions}

    # # There should be 3 reviews per forum.
    # reviews = openreview.tools.iterget_notes(
    #     client, invitation='ICLR.cc/2019/Conference/-/Paper.*/Official_Review')
    # reviews_by_forum = defaultdict(list)
    # for review in reviews:
    #     reviews_by_forum[review.forum].append(review)

    # # Because of the way the Program Chairs chose to run ICLR '19, there are no "decision notes";
    # # instead, decisions are taken directly from Meta Reviews.
    # meta_reviews = openreview.tools.iterget_notes(
    #     client, invitation='ICLR.cc/2019/Conference/-/Paper.*/Meta_Review')
    # meta_reviews_by_forum = {n.forum: n for n in meta_reviews}

    # Build a list of metadata.
    # For every paper (forum), get the review ratings, the decision, and the paper's content.
    metadata = []
    for forum in submissions_by_forum:

        # forum_reviews = reviews_by_forum[forum]
        # review_ratings = [n.content['rating'] for n in forum_reviews]

        # forum_meta_review = meta_reviews_by_forum[forum]
        # decision = forum_meta_review.content['recommendation']

        submission_content = submissions_by_forum[forum].content

        forum_metadata = {
            'forum': forum,
            # 'review_ratings': review_ratings,
            # 'decision': decision,
            'submission_content': submission_content
        }
        print(submission_content['title'])
        metadata.append(forum_metadata)

    # print('writing metadata to file...')
    # # write the metadata, one JSON per line:
    # with open(os.path.join(outdir, 'iclr19_metadata.jsonl'), 'w') as file_handle:
    #     for forum_metadata in metadata:
    #         file_handle.write(json.dumps(forum_metadata) + '\n')

    # if requested, download pdfs to a subdirectory.
    if get_pdfs:
        pdf_outdir = os.path.join(outdir, 'iclr20_pdfs')
        if not os.path.exists(pdf_outdir) :
            os.makedirs(pdf_outdir)
        for forum_metadata in tqdm(metadata, desc='getting pdfs'):
            pdf_binary = client.get_pdf(forum_metadata['forum'])
            pdf_outfile = os.path.join(pdf_outdir, '{}.pdf'.format(forum_metadata['forum']))
            with open(pdf_outfile, 'wb') as file_handle:
                file_handle.write(pdf_binary)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--outdir', default='C:\Users\hexu0003\Desktop', help='directory where data should be saved')
    parser.add_argument(
        '--get_pdfs', default=False, action='store_true', help='if included, download pdfs')
    parser.add_argument('--baseurl', default='https://api.openreview.net')
    parser.add_argument('--username', default='', help='defaults to empty string (guest user)')
    parser.add_argument('--password', default='', help='defaults to empty string (guest user)')

    args = parser.parse_args()

    outdir = args.outdir

    client = openreview.Client(
        baseurl=args.baseurl,
        username='hexu0003@e.ntu.edu.sg',
        password='Hexu1995')

    # download_iclr19(client, outdir, get_pdfs=True) #args.get_pdfs)
    
    print('getting metadata...')
    # get all ICLR '19 submissions, reviews, and meta reviews, and organize them by forum ID
    # (a unique identifier for each paper; as in "discussion forum").
    # submissions = openreview.tools.iterget_notes(
    #     client, invitation='ICLR.cc/2021/Conference/-/Blind_Submission')
    # submissions_by_forum = {n.forum: n for n in submissions}
    
    blind_notes = {note.id: note for note in openreview.tools.iterget_notes(client, invitation = 'ICLR.cc/2021/Conference/-/Blind_Submission', details='original')}
    # To download accpeted papers. Worked in iclr21.
    accepted_submissions = {}
    for note_id in blind_notes:
        note = blind_notes[note_id]
        try:
            note.content['venue']
            accepted_submissions[note_id] = note
        except:
            pass
   submissions_by_forum = accepted_submissions
    # Build a list of metadata.
    # For every paper (forum), get the review ratings, the decision, and the paper's content.
    metadata = []
    for forum in submissions_by_forum:

        submission_content = submissions_by_forum[forum].content

        forum_metadata = {
            'forum': forum,
            # 'review_ratings': review_ratings,
            # 'decision': decision,
            'submission_content': submission_content
        }
        # print(submission_content['title'])
        metadata.append(forum_metadata)

    # if requested, download pdfs to a subdirectory.
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    filter_list = ['reinforcement', 'Reinforcement','Policy','policy', 'Actor', 'critic', 'actor', 'Critic']
    pdf_outdir = os.path.join(outdir, 'iclr21_pdfs')
    if not os.path.exists(pdf_outdir) :
        os.makedirs(pdf_outdir)
    for forum_metadata in tqdm(metadata, desc='getting pdfs'):
        title = re.sub(rstr, "", str(forum_metadata['submission_content']['title']))
        title.replace('\n', '')
        down = False
        for f in filter_list:
            if f in title:
                down = True
                break
        if down:
            pdf_binary = client.get_pdf(forum_metadata['forum'])
            pdf_outfile = os.path.join(pdf_outdir, '{}.pdf'.format(title))
            with open(pdf_outfile, 'wb') as file_handle:
                file_handle.write(pdf_binary)
                
                
                
                