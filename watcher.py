import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  
import sys, subprocess

watchdog_watch_path = ''

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.less"]

    def process(self, event):
        print event.src_path, event.event_type
        subprocess.call('lessc ' + watchdog_watch_path + '/style.less' + ' ' + watchdog_watch_path + '/style.css', shell=True)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    
    # Only one running instance allowed
    import fcntl, sys
    pid_file = 'the_less_watcher.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print "An instance of the less watcher is already running. Terminating."
        sys.exit(0)

    args = sys.argv[1:]
    observer = Observer()
    watchdog_watch_path = args[0]
    observer.schedule(MyHandler(), path=args[0] if args else '.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
