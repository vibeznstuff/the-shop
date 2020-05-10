import seaborn as sns
import matplotlib.pyplot as plt 
import pandas as pd 


def one_way_frequencies(df, features, save_plots=False, plot_path=None):

    for feature in features:
        #f, ax = plt.subplots(figsize=(12,12))
        plt.title('{} Frequencies'.format(feature))
        sns.countplot(y=feature, data=df, color='c')
        
        if save_plots:
            plt.savefig('{0}/{1}_frequencies.png'.format(plot_path, feature),bbox_inches='tight')
        
        plt.close()


def histograms(df, features, save_plots=False, plot_path=None):

    for feature in features:
        #f, ax = plt.subplots(figsize=(12,12))
        plt.title('{} Histogram'.format(feature))
        sns.distplot(df[feature], norm_hist=True)
        
        if save_plots:
            plt.savefig('{0}/{1}_histogram.png'.format(plot_path, feature),bbox_inches='tight')
        
        plt.close()