def plot_single(in_file, zfunc, zname, out_file):

    import pylab
    import numpy
    import h5py
    from matplotlib.collections import PolyCollection
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import os

    print(out_file)
    if os.path.isfile(out_file):
        return

    with h5py.File(in_file,'r+') as f:
        vert_idx_list = numpy.concatenate(([0],
                                           numpy.cumsum(f['Number of vertices in cell'])))
        x_verts = numpy.array(f['x position of vertices'])
        y_verts = numpy.array(f['y position of vertices'])
        verts = []
        for i in range(len(f['density'])):
            lowbound = int(vert_idx_list[i])
            upbound = int(vert_idx_list[i+1])
            verts.append([[x,y] for x,y
                          in zip(x_verts[lowbound:upbound], 
                                 y_verts[lowbound:upbound])])
        coll = PolyCollection(verts, 
                              array=zfunc(f),
                              cmap = mpl.cm.jet,
                              edgecolors = 'none')
        fig, ax = plt.subplots()
        fig.suptitle(zname+' @ t = '+str(numpy.array(f['time'])[0]))
        ax.add_collection(coll)
        ax.autoscale_view()
        ax.set_aspect('equal')
        fig.colorbar(coll,ax=ax)
        print(out_file)
        if out_file==None:
            plt.show()
        else:
            plt.savefig(out_file)
        plt.clf()
        plt.cla()
        plt.close()

def plot_all(zfunc, zname):

    jl_flag = True

    import glob
    import numpy
    if jl_flag:
        import joblib

    flist = glob.glob('snapshot_*.h5')

    if jl_flag:
        joblib.Parallel(n_jobs=8)(joblib.delayed(plot_single)
                                  (fname,
                                   zfunc,
                                   zname,
                                   fname.replace('snapshot',zname).replace('.h5','.png')) for fname in flist)
    else:
        [plot_single(fname,zfunc,zname,
                     fname.replace('snapshot',zname).replace('.h5','.png'))
         for fname in flist]

def log10_density(f):

    import numpy

    return numpy.log10(numpy.array(f['density']))

def log10_pressure(f):

    import numpy

    return numpy.log10(f['pressure'])

def x_velocity(f):

    import numpy

    return numpy.array(f['x_velocity'])

def y_velocity(f):

    import numpy

    return numpy.array(f['y_velocity'])

def main():

    import matplotlib
    matplotlib.use('Agg')

    import numpy

    #plot_single('snapshot_0.h5',
    #            log10_temperature,
    #            'log10_temperature',
    #            'log10_temperature_0.png')

    plot_all(log10_density, 'log10_density')
    plot_all(log10_pressure, 'log10_pressure')
    plot_all(x_velocity, 'x_velocity')
    plot_all(y_velocity, 'y_velocity')
    #plot_all(He4_prof, 'He4')
    #plot_all(C12_prof, 'C12')
    #plot_all(O16_prof, 'O16')
    #plot_all(S32_prof, 'S32')
    #plot_all(Ne20_prof, 'Ne20')
    #plot_all(Mg24_prof, 'Mg24')
    #plot_all(Si28_prof, 'Si28')
    #plot_all(Ar36_prof, 'Ar36')
    #plot_all(Ca40_prof, 'Ca40')
    #plot_all(Ti44_prof, 'Ti44')
    #plot_all(Cr48_prof, 'Cr48')
    #plot_all(Fe52_prof, 'Fe52')
    #plot_all(Ni56_prof, 'Ni56')

if __name__ == '__main__':

    main()
