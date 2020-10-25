class DisplayOpts:
  def __init__(self):
    self.showPlot = False
    self.showTrack = False
    self.showRawData = False

    self.minId = 0
    self.maxId = 0
    self.sampleRate = 1

    self.xaxis = None
    self.yaxis = []
    self.multiy = False