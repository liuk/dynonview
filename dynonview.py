import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
from utils import DisplayOpts

@st.cache(persist=True)
def load_data(datafile):
  data = pd.read_csv(datafile)

  # data preprocessing
  data.dropna(axis=1, how='all', inplace=True)

  return data

def main():

  st.sidebar.write('## Load data')
  allfiles = [f for f in os.listdir(os.curdir) if '.csv' in f]
  datafile = st.sidebar.selectbox('', allfiles)

  # load data from a list of files
  data = load_data(datafile)
  
  if data is not None:
    # obtain the display configuration
    opts = displayConfig(data)

    if opts.showPlot:
      displayPlot(data, opts)

    if opts.showRawData:
      st.write(data.loc[opts.minId:opts.maxId:opts.sampleRate, [opts.xaxis]+opts.yaxis].reset_index(drop=True))

    if opts.showTrack:
      displayTrack(data.loc[opts.minId:opts.maxId:opts.sampleRate, :])

def displayConfig(data):

  st.sidebar.write('## Display configuration')
  
  datarange = st.sidebar.slider('', 0, len(data.index), (0, 100))
  sampleRate = st.sidebar.number_input('Sample Rate', 1, 100, 10, step=10)
  st.sidebar.write('Range of data to display: ', datarange[0], datarange[1])

  showplot = st.sidebar.checkbox('Show plot')
  multiy   = st.sidebar.checkbox('Multiple Y-axis')

  xaxis = st.sidebar.selectbox('X-axis', data.columns, index=3)

  n_overlays = st.sidebar.selectbox('Number of overlays', [1, 2, 3, 4], index=0)
  yaxis = []
  for i in range(n_overlays):
    yaxis.append(st.sidebar.selectbox('Y-axis %d' % (i+1), data.columns, index=6+i))

  opts = DisplayOpts()

  opts.showPlot = showplot
  opts.multiy = multiy 

  opts.minId = datarange[0]
  opts.maxId = datarange[1]
  opts.sampleRate = sampleRate

  opts.xaxis = xaxis
  opts.yaxis = yaxis

  st.sidebar.write('## Auxiliary information')
  opts.showRawData = st.sidebar.checkbox('Show data')
  opts.showTrack   = st.sidebar.checkbox('Show track')

  return opts

def displayPlot(data, opts):
  fig = go.Figure()

  for idx in range(len(opts.yaxis)):
    addPlot(idx, fig, data, opts)

  fig.update_layout(autosize=True, width=1000, height=500)
  fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
  fig.update_layout(xaxis_title=opts.xaxis)
  #fig.update_yaxes(scaleanchor='x', scaleratio=0.5)
  if len(opts.yaxis) == 1:
    fig.update_layout(yaxis_title=opts.yaxis[0])
  
  st.plotly_chart(fig, use_container_width=True)

def addPlot(idx, fig, data, opts):
  # remove rows with NaN in it
  subdata = data.loc[opts.minId:opts.maxId:opts.sampleRate, [opts.xaxis, opts.yaxis[idx]]].dropna(axis=0, how='any')

  # add traces depending on multi-y setting
  if not opts.multiy:
    fig.add_trace(go.Scatter(x=subdata[opts.xaxis], y=subdata[opts.yaxis[idx]], mode='markers', name=opts.yaxis[idx]))
  # else:
  #   if idx == 0:
  #     fig.add_trace(go.Scatter(x=subdata[opts.xaxis], y=subdata[opts.yaxis[idx]], mode='markers', name=opts.yaxis[idx]))
  #     fig.update_layout(yaxis=dict(title=opts.yaxis[idx], titlefont=dict(size=10), tickfont=dict(size=10)))
  #   else:
  #     fig.add_trace(go.Scatter(x=subdata[opts.xaxis], y=subdata[opts.yaxis[idx]], mode='markers', name=opts.yaxis[idx], yaxis='y'+str(idx+1)))
  #     fig.update_layout(yaxis2=dict(title=opts.yaxis[idx], anchor='free', overlaying='y', side='left', position=0.1))
      


def displayTrack(data):
  st.map(data.rename(columns={'Longitude (deg)': 'lon', 'Latitude (deg)': 'lat'}), use_container_width=True)

if __name__ == '__main__':
  st.title('Dynon Skyview Log Viewer')
  main()