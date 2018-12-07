from PIL import Image
import numpy as np
from scipy.spatial import distance
import pickle
import scipy.spatial.distance as distance
from cyvlfeat.sift.dsift import dsift
from time import time
import pdb

def get_bags_of_sifts(image_paths):
    ############################################################################
    # TODO:                                                                    #
    # This function assumes that 'vocab.pkl' exists and contains an N x 128    #
    # matrix 'vocab' where each row is a kmeans centroid or visual word. This  #
    # matrix is saved to disk rather than passed in a parameter to avoid       #
    # recomputing the vocabulary every time at significant expense.            #

    # image_feats is an N x d matrix, where d is the dimensionality of the     #
    # feature representation. In this case, d will equal the number of clusters#
    # or equivalently the number of entries in each image's histogram.         #

    # You will want to construct SIFT features here in the same way you        #
    # did in build_vocabulary.m (except for possibly changing the sampling     #
    # rate) and then assign each local feature to its nearest cluster center   #
    # and build a histogram indicating how many times each cluster was used.   #
    # Don't forget to normalize the histogram, or else a larger image with more#
    # SIFT features will look very different from a smaller version of the same#
    # image.                                                                   #
    ############################################################################
    '''
    Input :
        image_paths : a list(N) of training images
    Output :
        image_feats : (N, d) feature, each row represent a feature of an image
    '''
    image_feats = None
    with open('vocab.pkl', 'rb') as voc:
        vocal_feats = pickle.load(voc)

    record = np.zeros(vocal_feats.shape[0])
    image_feats = np.zeros((len(image_paths), vocal_feats.shape[0]))

    for i, path in enumerate(image_paths):
        img = np.asarray(Image.open(path),dtype='float32')
        frames, descriptors = dsift(img, step=[5,5], fast=True)
        L2_dis = distance.cdist(vocal_feats, descriptors, 'euclidean')
        for j in range(descriptors.shape[0]):
            min_index = np.argmin(L2_dis[:, j])
            record[min_index] = record[min_index] + 1
        average = np.mean(record)
        deviate = np.std(record)
        img_normal = (record - average) / deviate
        image_feats[i, :] = img_normal
        record = np.zeros(vocal_feats.shape[0])
    #############################################################################
    #                                END OF YOUR CODE                           #
    #############################################################################
    return image_feats
