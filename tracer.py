from psutil import Process
from gdb import Gdb
from datetime import datetime

class Tracer:
    def __init__(self, pid):
        self.process = Process(pid)
        self.gdb = Gdb(pid)
        self.io_read_bytes = 0
        self.io_write_bytes = 0
        self.about = (self.process.name, pid, datetime.now())

    def snapshot(self):
        cpu = self.process.get_cpu_percent()
        mem = self.process.get_memory_info()[0] # only RSS for now
        io = self.get_io_bytes()
        stack = self.gdb.get_stack()
        return (cpu, mem, io, stack)

    def get_io_bytes(self):
        _, _, read_bytes, write_bytes = self.process.get_io_counters()
        io = (read_bytes - self.io_read_bytes, write_bytes - self.io_write_bytes)
        self.io_read_bytes, self.io_write_bytes = read_bytes, write_bytes
        return io

if __name__ == '__main__':
    t = Tracer(29119)
    print t.snapshot()
