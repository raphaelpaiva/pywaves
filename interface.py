import threading
import tkinter

from tkinter.ttk import Frame
from tkinter.ttk import Label
from tkinter.ttk import LabelFrame
from tkinter.ttk import Scale
from tkinter.ttk import Button

from sinusoud import Sinusoid
from oscilator import Oscilator
from player import Player

class Window(Frame):
  def __init__(self, master=None):
    Frame.__init__(
      self,
      master
    )
    self.master = master
    self.stop   = False
    
    self.oscilators    = [
      Oscilator(name="OSC1", wave=Sinusoid()),
      Oscilator(name="OSC2", wave=Sinusoid(frequency=880.0))
    ]
    
    self.player        = Player()
    self.player_thread = threading.Thread(target=self._continuous_play)
    
    self._create_window()
    
    self.player_thread.start()

  def _create_window(self):
    self.master.title("JustASynth")
    
    osc_frames = self._create_osc()
    for frame in osc_frames:
      frame.grid()

    master_frame = self._create_master()
    master_frame.grid(row=0, column=1)
    
    self.grid()
  
  def _create_master(self):
    master_frame = LabelFrame(
      self,
      text="Master",
      relief=tkinter.GROOVE,
      borderwidth=5
    )

    Label(
      master_frame,
      text="Volume"
    ).grid()

    vol_tracker = tkinter.DoubleVar()
    vol_tracker.set(self.player.volume)

    Scale(
      master_frame,
      variable=vol_tracker,
      from_=1.0,
      to=0.0,
      orient=tkinter.VERTICAL,
      command=self.player.set_volume,
    ).grid()

    Label(
      master_frame,
      text=f"Channels: {self.player.channels}"
    ).grid(sticky=tkinter.W)

    Label(
      master_frame,
      text=f"Sample Size: {self.player.sample_size}"
    ).grid(sticky=tkinter.W)

    Label(
      master_frame,
      text=f"Sample Rate: {self.player.sample_rate}Hz"
    ).grid(sticky=tkinter.W)

    return master_frame

  def _create_osc(self):
    osc_frames = []
    
    for osc in self.oscilators:
      osc_frame = LabelFrame(
        self,
        text=osc.name,
        relief=tkinter.GROOVE,
        borderwidth=5
      )
      
      freq_tracker = tkinter.DoubleVar()
      freq_tracker.set(float(osc.wave.frequency))

      Label(
        osc_frame,
        text="Frequency"
      ).grid(row=1, column=0)

      Label(
        osc_frame,
        textvariable=freq_tracker
      ).grid(row=0, column=1)
      
      Scale(
        osc_frame,
        variable=freq_tracker,
        from_=20,
        to=5000,
        orient=tkinter.HORIZONTAL,
        command=osc.set_frequency,
        length=400
      ).grid(row=1, column=1)

      vol_tracker = tkinter.DoubleVar()
      vol_tracker.set(float(osc.volume))

      Label(
        osc_frame,
        text="Volume"
      ).grid(row=3, column=0)

      Label(
        osc_frame,
        textvariable=vol_tracker
      ).grid(row=2, column=1)

      Scale(
        osc_frame,
        variable=vol_tracker,
        from_=0.0,
        to=1.0,
        orient=tkinter.HORIZONTAL,
        command=osc.set_volume,
      ).grid(row=3, column=1, sticky=tkinter.W)

      osc_frames.append(osc_frame)
    
    return osc_frames

  def _continuous_play(self):
    t = 0
    while not self.stop:
      sample_size = self.player.sample_size
      sample_rate = self.player.sample_rate
      duration    = sample_size / sample_rate
      time        = t * duration
      
      samples = []

      for osc in self.oscilators:
        sample, _ = osc.wave.sample(duration, sample_rate, start_time=time)
        samples.append(sample)

      master = self.player.mix(samples)

      self.player.play_sample(master)

      t += 1

  def terminate(self):
    self.stop = True
    self.player_thread.join()
    self.player.terminate()


def main():
  root = tkinter.Tk()

  root.geometry("")

  app = Window(root)
  
  root.mainloop()

  app.terminate()

if __name__ == "__main__":
  main()

