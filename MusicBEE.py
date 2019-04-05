import sys
import pexpect
import helperbee

class MusicBEE():
    def __init__(self):
        if sys.platform == "darwin":
            cmd = "vlc -I rc"
        else:
            cmd = "vlc"

        self.proc = pexpect.spawn(cmd)
        self.proc.expect("> ")

    def _clear_playlist(self):
        self.proc.sendline("clear")
        self.proc.expect("> ")
    
    def _queue_song(self, filename):
        song_path = helperbee.helper.get_resources_path() + "/music/" + filename
        self.proc.sendline("enqueue {}".format(song_path))
        self.proc.expect("> ")

    def _play_playlist(self):
        self.proc.sendline("play")
        self.proc.expect("> ")

    def play_playlist(self, filenames):
        self._clear_playlist()
        for name in filenames:
            self._queue_song(name)
        self._play_playlist()

    def play_song(self, filename):
        self._clear_playlist()
        self._queue_song(filename)
        self._play_playlist()

    def pause(self):
        self.proc.sendline("pause")
        self.proc.expect("> ")
    
    def set_volume(self, val):
        if not(0 <= val <= 256):
            return
        self.proc.sendline("volume {}".format(str(int(val))))
        self.proc.expect("> ")

player = MusicBEE()