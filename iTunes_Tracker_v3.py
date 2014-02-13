import win32com.client, pythoncom, time
from pprint import pprint
from datetime import datetime

startupinfo = None

def main():
	
    itunes = win32com.client.Dispatch("iTunes.Application")
    itunesEvents = win32com.client.WithEvents(itunes, itunesEventHandler)
	
    while True:
        time.sleep(0.1)
        pythoncom.PumpWaitingMessages()
        if itunesEvents.quitting:
            print("Ending script...")
            del itunesEvents
            del itunes
            break

class itunesEventHandler():
	
    old_track = ""
    old_count = 0
	
    def __init__(self):
        self.quitting = False

    def OnPlayerPlayEvent(self, track):
		self.play_count_change(self.old_count, self.old_track)
		track = win32com.client.CastTo(track, 'IITTrack')
		self.old_track = track
		self.old_count = track.PlayedCount
		print("Play event received!", type(track), track.Name)
    
    def play_count_change(self, old_count, track):
		if track != "":
			new_count = track.PlayedCount
		
			if new_count == old_count + 1:
				 with open("details.txt", "a") as f:
					f.write("%s, %s, %s, %s, %s, %s, %s, %s\n" %(track.Name, track.Artist, track.Album, track.Genre, track.Rating, new_count, track.DateAdded, str(datetime.now())))
					print "It Worked!"
	
    def OnAboutToPromptUserToQuitEvent(self): 
        print("Quitting")
        self.quitting = True

    def OnQuittingEvent(self):
        print("Quitting")
        self.quitting = True

if __name__ == '__main__':
    main()