from PIL import Image
from wordcloud import WordCloud
from collections import Counter
from azure.storage.blob import BlockBlobService, PublicAccess

import numpy as np
import matplotlib
import cv2

matplotlib.use('agg')
import matplotlib.pyplot as plt


def download_from_blob():
    """ Download word counting result from blob. """
    block_blob_service = BlockBlobService(account_name='project3twitter',
                                          account_key='<YOUR_ACCOUNT_KEY>')
    container_name = 'project3'
    block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

    # actual download
    block_blob_service.get_blob_to_path(container_name, 'word-count.txt', 'resource/word-count.txt')


def get_word_frequency():
    """ Count word frequency to Counter. """
    counter = Counter()
    with open('resource/word-count.txt', encoding="utf8") as f:
        for line in f.readlines():
            try:
                word, count = line.split(':')
                if (word == "RT"):
                    continue
                count = int(count)
                counter[word] += count
            except Exception as e:
                continue
    return counter


def make_image():
    """ Generate image from the word counter. """
    # get the mask
    twitter_mask = np.array(Image.open('resource/twitter-mask.png'))

    wc = WordCloud(background_color='white', max_words=100, mask=twitter_mask, contour_width=3,
                   contour_color='steelblue')

    # generate word cloud
    wc.generate_from_frequencies(get_word_frequency())

    # store to file
    wc.to_file('/tmp/twitter.png')

    # show
    frame = cv2.imread('/tmp/twitter.png')
    cv2.imshow('figure', frame)
    cv2.waitKey(60000)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    while True:
        download_from_blob()
        make_image()
