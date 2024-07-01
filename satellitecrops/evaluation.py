from tensorflow.keras.metrics import MeanIoU, IoU

import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np
import pandas as pd

def metrics(n_classes:int, ignore_class:int=0, sparse_y_pred:bool=False, sparse_y_true:bool=False):
    '''
    Returns a list of metrics containing the mean Intersection-Over-Union metric (meanIoU) and the IoU for each predicted class.

    n_classes: The possible number of labels the prediction task can have.
    sparse_y_pred: Whether predictions are encoded using integers or dense floating point vectors.
    sparse_y_true: Whether labels are encoded using integers or dense floating point vectors.
    ignore_class: Optional integer. The ID of a class to be ignored during meanIoU computation.
    '''

    l = [MeanIoU(num_classes=n_classes, sparse_y_pred=sparse_y_pred, sparse_y_true=sparse_y_true, ignore_class=ignore_class)]

    for i in range(n_classes):
        l.append(IoU(num_classes=n_classes,
                     target_class_ids=[i],
                     sparse_y_pred=sparse_y_pred,
                     sparse_y_true=sparse_y_true))

    return l

def ignore_class(y:np.ndarray, threshold:float=0.05):
    '''Returns a list of classes not significant (< Threshold). Includes by default 0 in the list which correspond to the background. '''
    unique, count = np.unique(y, return_counts=True)
    prop = np.round(count / count.sum() * 100, 2)

    df = pd.DataFrame({'Id':unique, 'Prop':prop}).sort_values('Prop', ascending=False)

    l = df[df.Prop < threshold].Id.to_list()
    l.append(0)
    return l

def plot_multiple_lc(history:dict, classes:list, mapping:dict):
    '''
    Plots the learning curves with the loss, the mean_IoU and IoU of the classes that you want.

    history: Result of the model.fit().
    classes: The targeted labels for which we want to plot the IoU.
    mapping: The dictionnary mapping between the labels and their names.
    '''

    n_classes = len(mapping)

    keys = list(history.history.keys())

    # Instantiate the figure
    fig, axs = plt.subplot_mosaic('AC;BB')

    fig.set_figheight(13)
    fig.set_figwidth(13)
    fig.suptitle('Learning curves')

    # Plot the loss
    axs['A'].plot(history.history['loss'], label='Train')
    axs['A'].plot(history.history['val_loss'], label='Validation')
    axs['A'].set_title('Loss')
    axs['A'].legend()

    # Plot the IoU of the targeted classes
    for i in classes:
        axs['B'].plot(history.history[keys[i]], label=f'Train - {mapping[i]}')
        axs['B'].plot(history.history[f'val_{keys[i]}'], label=f'Validation - {mapping[i]}')

    axs['B'].set_title('IoU per class')
    axs['B'].legend(loc='right')

    # Plot the meanIoU
    axs['C'].plot(history.history[keys[n_classes+1]], label='Train')
    axs['C'].plot(history.history[keys[-1]], label='Validation')
    axs['C'].set_title('Mean IoU')
    axs['C'].legend()

    fig.show()


def analyse_proportions(y_truth:list, y_pred:list,mapping:dict):
    '''
    Returns a dataframe with the proportion of each label both for the ground truth and the prediction.

    y_truth: Dense ground truth labels.
    y_pred: Dense prediction labels.
    mapping: The dictionnary mapping between the labels and their names.

    '''

    #Calculate proportions for ground truth
    unique_truth, counts_truth = np.unique(y_truth, return_counts=True)
    prop_truth = np.round(counts_truth / counts_truth.sum() * 100, 1)

    # Calculate proportions for predictions
    unique_pred, counts_pred = np.unique(y_pred, return_counts=True)
    prop_preds = np.round(counts_pred / counts_pred.sum() *100, 1)

    # Creating the dataframe
    df_truth = pd.DataFrame({'Id':unique_truth, 'Truth':prop_truth})
    df_pred = pd.DataFrame({'Id':unique_pred, 'Pred':prop_preds})

    df = df_truth.merge(df_pred, on='Id', how='outer').fillna(0).sort_values('Truth', ascending=False)

    df.set_index('Id', inplace=True)
    a = pd.Series(df.index.map(mapping))
    df.insert(0, 'Category', a)

    return df


def plot_comparison(y_truth:list, y_pred:list, mapping:dict):
    '''
    Plots the ground truth, the prediction and the difference (green corresponding to well predicted) for three random images.

    y_truth: Dense ground truth labels.
    y_pred: Dense prediction labels.
    mapping: The dictionnary mapping between the labels and their names.
    '''

    n_classes = len(mapping)

    colors = ['mediumseagreen', 'tomato']
    bounds = [0,1]

    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    colors = ['blue',
            'lightsteelblue',
            'cornflowerblue',
            'slategrey',
            'lavender',
            'salmon',
            'orange',
            'red',
            'orangered',
            'sienna',
            'darkslategray',
            'darkcyan',
            'aqua',
            'skyblue',
            'pink',
            'wheat',
            'bisque',
            'forestgreen',
            'yellow',
            'powderblue',
            'rosybrown']
    bounds = np.arange(n_classes)

    cmapbis = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmapbis.N)

    fig, axs = plt.subplot_mosaic('ABC;DEF;HIJ')

    fig.set_figheight(10)
    fig.set_figwidth(13)
    fig.suptitle('Comparison predictions with ground truth')

    random_val = np.random.randint(0, X_test.shape[0],3)

    axs['A'].imshow(y_truth[random_val[0]], cmap=cmapbis, norm=norm)
    axs['A'].set_title('Ground truth')
    axs['B'].imshow(y_pred[random_val[0]], cmap=cmapbis, norm=norm)
    axs['B'].set_title('Prediction')
    a = y_truth[random_val[0]] - y_pred[random_val[0]]
    axs['C'].imshow(np.where(a == 0, a, 1), cmap=cmap, norm=norm)
    axs['C'].set_title('Difference')

    axs['D'].imshow(y_truth[random_val[1]], cmap=cmapbis, norm=norm)
    axs['E'].imshow(y_pred[random_val[1]], cmap=cmapbis, norm=norm)
    a = y_truth[random_val[1]] - y_pred[random_val[1]]
    axs['F'].imshow(np.where(a == 0, a, 1), cmap=cmap, norm=norm)

    axs['H'].imshow(y_truth[random_val[2]], cmap=cmapbis, norm=norm)
    axs['I'].imshow(y_pred[random_val[2]], cmap=cmapbis, norm=norm)
    a = y_truth[random_val[2]] - y_pred[random_val[2]]
    axs['J'].imshow(np.where(a == 0, a, 1), cmap=cmap, norm=norm)

    # Create custom legend
    legend_elements = [mpl.patches.Patch(facecolor=colors[i], edgecolor='black', label=str(mapping[i])) for i in range(n_classes)]

    # Adjust the layout to make space for the legend
    plt.subplots_adjust(right=0.8)

    # Place legend outside the right side of the plot
    fig.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(0.82, 0.5), title='Classes')

    fig.show()
