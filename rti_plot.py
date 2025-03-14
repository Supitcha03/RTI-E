# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 10:48:27 2021

@author: krong
"""
import os
from datetime import datetime
import numpy as np
from rti_rec import RecordIndex
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def plotRTIIm(scheme, iM, **kw):
     
    filename = ''
    (min_vl, max_vl) = (0, 1)
    if 'filename' in kw:
        filename = kw['filename']
    title = ''
    if 'title' in kw:
        title = kw['title']
    label = ''
    if 'label' in kw:
        label = kw['label']
    sensorPosition = scheme.getSensorPosition()
    if 'sensorPosition' in kw:
        sensorPosition = kw['sensorPosition']
    color='coolwarm'
    if 'color' in kw:
        color = kw['color']
    s_sensor = True
    if 'show_sensor' in kw:
        s_sensor = kw['show_sensor']
    s_marker = 's'
    if 'sensor_marker' in kw:
        s_marker = kw['sensor_marker']
    s_color = 'black'
    if 'sensor_color' in kw:
        s_color = kw['sensor_color']
    if 'atten_range' in kw:
        (min_vl, max_vl) = kw['atten_range']
    
    sel = scheme.selection
    coordX = np.asarray(sel.coordX)
    coordY = np.asarray(sel.coordY)

     
    fig, ax = plt.subplots(1, 1)
    ax.set_title(title, pad=10)
    ax.set_ylabel('Y[m]')
    xlabel = 'X[m]'
    if 'rmse' in kw: xlabel += '\nRMSE = ' + '{:.3f}'.format(kw['rmse'])
    if 'mse' in kw: xlabel += '\nMSE = ' + '{:.3f}'.format(kw['mse'])
    ax.set_xlabel(xlabel)

    
    hm = ax.imshow(iM.T,
                   extent=[coordX[0], coordX[-1], coordY[0], coordY[-1]],
                   cmap=color,
                   origin='lower',
                   interpolation='nearest',
                   vmin=min_vl,
                   vmax=max_vl)

    cb = plt.colorbar(hm)
    plt.grid()
    if label: cb.set_label(label)
    if s_sensor and len(sensorPosition) > 0:
        plt.scatter(sensorPosition[0],
                    sensorPosition[1],
                    s=150,
                    c=s_color,
                    marker=s_marker)
    
    
    if filename:
        if 'path' in kw:
            fn = os.sep.join([kw['path'], 
                             (filename + '.svg')])
        else:
            fn = (filename + '.svg')
        plt.savefig(fn)    
        
        if 'save' in kw:
            tStr = datetime.now().strftime('-%H%M%S')
            fn_csv = os.sep.join([kw['save'], 
                             ('img_' + filename + tStr + '.csv')])
            if 'atten' in kw:
                fn_inp = os.sep.join([kw['save'], 
                                 ('input_'+ 
                                  filename + tStr + '.csv')])
                np.savetxt(fn_inp, kw['atten'], delimiter = ',', fmt = '%s')
            np.savetxt(fn_csv, iM.T, 
                       delimiter = ',', fmt = '%s')

    plt.show(block=False)
    return fig

def plotDerivative(scheme, de, **kw):
    filename = ''
    if 'filename' in kw:
        filename = kw['filename']
    title = ''
    if 'title' in kw:
        title = kw['title']
    label = ''
    if 'label' in kw:
        label = kw['label']
    sensorPosition = scheme.getSensorPosition()
    if 'sensorPosition' in kw:
        sensorPosition = kw['sensorPosition']
    color='Blues'
    if 'color' in kw:
        color = kw['color']
    s_sensor = True
    if 'show_sensor' in kw:
        s_sensor = kw['show_sensor']
    s_marker = 's'
    if 'sensor_marker' in kw:
        s_marker = kw['sensor_marker']
    s_color = 'black'
    if 'sensor_color' in kw:
        s_color = kw['sensor_color']
        
    sel = scheme.selection

    coordX = np.asarray(sel.coordX)
    coordY = np.asarray(sel.coordY)
    
    X, Y = np.meshgrid(coordX[0:-1] + scheme.vx_width/2, 
                       coordY[0:-1] + scheme.vx_length/2)
    
     
    fig, ax = plt.subplots(1, 1)
    hm = ax.imshow(de[RecordIndex.DERIVATIVE_ABS].T,
                   extent=[coordX[0], coordX[-1], coordY[0], coordY[-1]],
                   cmap=color,
                   origin='lower',
                   interpolation='nearest',
                   vmin=0)
    # norm = np.log10(de['abs'])
    U = (de[RecordIndex.DERIVATIVE_X]).T  #/de['abs']
    V = (de[RecordIndex.DERIVATIVE_Y]).T  #/de['abs']
    ax.quiver(X, Y, U, V,
              scale = 1.5,
              scale_units = 'xy',
              width = 0.010,
              headwidth = 3,
              headlength = 3,
              headaxislength = 2.5)
    
    ax.set_title(title, pad=10)
    ax.set_ylabel('Y[m]')
    xlabel = 'X[m]'
    if 'caption' in kw: xlabel += '\n' + kw['caption']
    ax.set_xlabel(xlabel)
    
    cb = plt.colorbar(hm)
    if label: cb.set_label(label)
    if s_sensor and len(sensorPosition) > 0:
        plt.scatter(sensorPosition[0],
                    sensorPosition[1],
                    s=150,
                    c=s_color,
                    marker=s_marker)
    plt.grid()
    if filename:
        if 'path' in kw:
            fn = os.sep.join([kw['path'], 
                             ('DE_' + filename + '.svg')])
        else:
            fn = (filename + '.svg')
        plt.savefig(fn)
        if 'save' in kw:
            tStr = datetime.now().strftime('-%H%M%S')
            fn_csv = os.sep.join([kw['save'], 
                             ('der_' + filename + tStr + '.csv')])
            if 'atten' in kw:
                fn_inp = os.sep.join([kw['save'], 
                                 ('input_'+ 
                                  filename + tStr + '.csv')])
                np.savetxt(fn_inp, kw['atten'], delimiter = ',', fmt = '%s')
            np.savetxt(fn_csv, de[RecordIndex.DERIVATIVE_ABS].T, 
                       delimiter = ',', fmt = '%s')

    plt.show(block=False)
    return fig

def plotSurface(scheme, Z, **kw):
    filename = ''
    if 'filename' in kw:
        filename = kw['filename']
    title = ''
    if 'title' in kw:
        title = kw['title']
    label = ''
    if 'label' in kw:
        label = kw['label']
    color = cm.coolwarm
    if 'color' in kw:
        color = kw['color']

     
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x = np.asarray(scheme.selection.coordX)
    y = np.asarray(scheme.selection.coordY)

    X, Y = np.meshgrid(x, y)

    # Plot the surface.
    surf = ax.plot_surface(X, 
                           Y, 
                           Z, 
                           cmap=color,
                           linewidth=0, 
                           antialiased=False)

    # Customize the z axis.
    mn = min(Z)
    mx = max(Z)
    ax.set_zlim(mn-0.05*abs(mn), mx + 0.05*abs(mx))

    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')
    ax.set_xlabel('x[m]')
    ax.set_ylabel('y[m]')
    if title: ax.set_title(title)
    # Add a color bar which maps values to colors.
    cb = fig.colorbar(surf,
                     shrink=0.5,
                     aspect=5)
    if label: cb.set_label(label)
    if filename:
        if 'path' in kw:
            fn = os.sep.join(kw['path'], 
                             (filename + '.svg'))
        else:
            fn = (filename + '.svg')
        plt.savefig(fn)
        if 'save' in kw:
            tStr = datetime.now().strftime('-%H%M%S')
            fn_csv = os.sep.join([kw['save'], 
                             ('surf_' + filename + tStr + '.csv')])
            if 'atten' in kw:
                fn_inp = os.sep.join([kw['save'], 
                                 ('input_'+ 
                                  filename + tStr + '.csv')])
                np.savetxt(fn_inp, kw['atten'], delimiter = ',', fmt = '%s')
            np.savetxt(fn_csv, Z, 
                       delimiter = ',', fmt = '%s')

    plt.show(block=False)
    return fig
    
def process_boxplot(data, **kw):
     
    fig, ax = plt.subplots(1,1)
    
    bp = plt.boxplot(data, 
                     patch_artist = True,
                     notch = True,
                     zorder=1)
    
    if 'title' in kw:
        ax.set_title(kw['title'], pad=10)
    if 'ticklabel' in kw:
        ax.set_xticklabels(kw['ticklabel'])
    if 'xlabel' in kw:
        ax.set_xlabel(kw['xlabel'])
    if 'ylabel' in kw:
        ax.set_ylabel(kw['ylabel'])
    
    plt.grid()
    
    colors = ['b', 'g',
              'r', 'violet', 
              'white', 'yellow']
 
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set(linewidth = 1.5)
    # changing color and linewidth of
    # whiskers
    for whisker in bp['whiskers']:
        whisker.set(color ='black',
                    linewidth = 2,
                    linestyle ="--")
     
    # changing color and linewidth of
    # caps
    for cap in bp['caps']:
        cap.set(color ='black',
                linewidth = 5)
     
    # changing color and linewidth of
    # medians
    for median in bp['medians']:
        median.set(color ='black',
                   linewidth = 3)
     
    # changing style of fliers
    for flier in bp['fliers']:
        flier.set(marker ='D',
                  markersize = 5,
                  color ='black',
                  alpha = 0.5)
    if 'filename' in kw:
        if 'path' in kw:
            fn = os.sep.join([kw['path'], 
                             (kw['filename'] + '.svg')])
        else:
            fn = (kw['filename'] + '.svg')
        plt.savefig(fn)
        if 'save' in kw:
            filename = kw['filename']
            tStr = datetime.now().strftime('-%H%M%S')
            fn_csv = os.sep.join([kw['save'], 
                             ('box_' + filename + tStr + '.csv')])
            if 'atten' in kw:
                fn_inp = os.sep.join([kw['save'], 
                                 ('input_'+ 
                                  filename + tStr + '.csv')])
                np.savetxt(fn_inp, kw['atten'], delimiter = ',', fmt = '%s')
            np.savetxt(fn_csv, data, 
                       delimiter = ',', fmt = '%s')

    plt.show(block=False)
    return fig

def process_plot(data, **kw):
     
    fig, ax = plt.subplots(1,1)
    
    makeR = ['o', 's', 'v', 'p', 'D', '1', '*', 'H']
    colorS = ['b', 'g', 'c',
              'r', 'violet', 'k', 
              'gray', 'yellow', 'orange']
    
    i = 0
    try:
        for k, e in data.items():
            if 'X' in kw: 
                plt.plot(kw['X'], e, 
                        c=colorS[i], 
                        marker = makeR[i],
                        label = k.name)
            else:
                plt.plot(e, 
                        c=colorS[i], 
                        marker = makeR[i],
                        label = k.name)            
            i += 1
        ax.legend()
    except:
        if 'graphindex' in kw:
            i = kw['graphindex']
        if 'X' in kw: 
            plt.plot(kw['X'], data, 
                    c=colorS[i], 
                    marker = makeR[i])
        else:
            plt.plot(data, 
                    c=colorS[i], 
                    marker = makeR[i])            
        
    if 'xscale' in kw:
        ax.set_xscale(kw['xscale'])
    if 'yscale' in kw:
        ax.set_yscale(kw['yscale'])
    if 'title' in kw:
        ax.set_title(kw['title'], pad=10)
    if 'ticklabel' in kw:
        ax.set_xticklabels(kw['ticklabel'])
    if 'xlabel' in kw:
        ax.set_xlabel(kw['xlabel'])
    if 'ylabel' in kw:
        ax.set_ylabel(kw['ylabel'])
    
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.xaxis.set_minor_formatter(FormatStrFormatter(""))
    ax.set_xticks(kw['X'])
    if 'tickformat' in kw:
        ax.set_xticklabels([kw['tickformat'] % x for x in kw['X']])    
    
    plt.grid()
    
    if 'filename' in kw:
        if 'path' in kw:
            fn = os.sep.join([kw['path'], 
                             (kw['filename'] + '.svg')])
        else:
            fn = (kw['filename'] + '.svg')
        plt.savefig(fn)
        if 'save' in kw:
            filename = kw['filename']
            tStr = datetime.now().strftime('-%H%M%S')
            fn_csv = os.sep.join([kw['save'], 
                             ('plot_' + filename + tStr + '.csv')])
            if 'atten' in kw:
                fn_inp = os.sep.join([kw['save'], 
                                 ('input_'+ 
                                  filename + tStr + '.csv')])
                np.savetxt(fn_inp, kw['atten'], delimiter = ',', fmt = '%s')
            np.savetxt(fn_csv, data, 
                       delimiter = ',', fmt = '%s')
    
    plt.show(block=False)
    return fig