import win32com.client, pythoncom, time
from pprint import pprint

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

    def __init__(self):
        self.quitting = False

    def OnPlayerPlayEvent(self, track):
        track = win32com.client.CastTo(track, 'IITTrack')
        print("Play event received!", type(track), track.Name)
		
    def OnDatabaseChangedEvent(self, deletedObjectIDs, changedObjectIDs):
        print("Database changed!", type(deletedObjectIDs), type(changedObjectIDs))
        for thing in changedObjectIDs:
            print(thing)

    def OnAboutToPromptUserToQuitEvent(self): 
        print("Quitting")
        self.quitting = True

    def OnQuittingEvent(self):
        print("Quitting")
        self.quitting = True

if __name__ == '__main__':
    main()