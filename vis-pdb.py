import numpy as np
import streamlit as st

import pandas as pd

from matplotlib import pyplot as plt
from matplotlib import collections

import io
from sklearn.manifold import TSNE

def mkfig(w, h):
  figsize = [w, h]
  subplot = {
    'left':   0.10,
    'right':  0.10,
    'bottom': 0.10,
    'top':    0.10,
    'wspace': 1.50,
    'hspace': 2.00,
    'grid': True,
  }
  with plt.style.context('matplotlibrc'):
    plt.rcParams["figure.figsize"]        = figsize
    plt.rcParams["figure.subplot.left"]   = subplot['left'] / figsize[0]
    plt.rcParams["figure.subplot.right"]  = 1.00 - subplot['right'] / figsize[0]
    plt.rcParams["figure.subplot.bottom"] = subplot['bottom'] / figsize[1]
    plt.rcParams["figure.subplot.top"]    = 1.00 - subplot['top'] / figsize[1]
    plt.rcParams["figure.subplot.wspace"] = subplot['wspace'] / figsize[0]
    plt.rcParams["figure.subplot.hspace"] = subplot['hspace'] / figsize[1]
    plt.rcParams["axes.grid"]             = subplot['grid']
    fig, ax = plt.subplots()
  return fig, ax

def main():

  st.title("PDB Visualizer")
  
  pdb_file = st.file_uploader("Read a PDB file")

  if pdb_file is not None:
    stringio = io.StringIO(pdb_file.getvalue().decode("utf-8"))
    xyz = np.array([[float(x) for x in line.split()[5:8]] for line in stringio.readlines() if ' CA ' in line])
    
    perplexity = st.slider('Perplexity', 5, len(xyz), 100)

    xy = TSNE(n_components = 2, random_state = 1, perplexity = perplexity).fit_transform(xyz)[:, ::-1]
    xy = np.array([[x[0], -x[1]] for x in xy])
    
    angle = st.slider('Rotate', -180, 180, 112)
    theta = angle * 3.14 / 180
    xy = np.array([[np.cos(theta) * x[0] - np.sin(theta) * x[1], np.sin(theta) * x[0] + np.cos(theta) * x[1]] for x in xy])

    node = pd.DataFrame(xy, columns=['x', 'y'])
    node['chain'] = ['A' for n in range(99)] + ['B' for n in range(99)] + ['C' for n in range(10)]
    node['resid'] = [n+1 for n in range(99)] + [n+1 for n in range(99)] + [n+1 for n in range(10)]
    
    fig, ax = mkfig(6.0, 4.0)

    for c in ['A', 'B', 'C']:
      ax.scatter(node[node['chain'] == c].x, node[node['chain'] == c].y, s = 25, alpha = 0.5, label = c)
    for n in range(len(xy)): ax.annotate(node.at[n, 'resid'], xy = xy[n], size = 6)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    for axis in ['top', 'left', 'bottom', 'right']:
      ax.spines[axis].set_linewidth(0.1)

    st.pyplot(fig)

    with io.BytesIO() as buffer:
      np.savetxt(buffer, xy)
      st.download_button (
        label="Download a node file",
        data = buffer,
        file_name = "node.txt",
        mime = "text/plain")

if __name__ == "__main__":
    main()
