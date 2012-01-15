from subprocess import Popen, PIPE

class Gdb:
    def __init__(self, pid):
        self.process = Popen(['gdb', '-p', str(pid)], stdin=PIPE, stdout=PIPE, stderr=open('/dev/null', 'w'))
        self.command('set prompt (gdb) \\n')
        self.command('set width 0')
        self.command('set height 0')
        self.command('set confirm off')
        self.ignore_signals()
        self.play()

    def __del__(self):
        self.process.terminate()
        
    def command(self, cmd):
        self.process.stdin.write(cmd + '\n')
        return self.read_to_prompt()

    def read_to_prompt(self):
        buf = ''
        while True:
            line = self.process.stdout.readline()
            if not line: break
            elif line.endswith('(gdb) \n'): break
            else: buf += line
        return buf

    def ignore_signals(self):
        for s in gdb_signals():
            self.command('handle %s nostop noprint pass' % s)

    def get_stack(self):
        self.pause()
        stack = self.command('info stack') # todo: detect and use noargs support
        self.play()
        lines = [ line for line in stack.split('\n') if line and line[0] == '#' ]
        return [ line.split(' ', 1)[1].strip() for line in lines ]

    def play(self):
        self.process.stdin.write('cont\n')
    
    def pause(self):
        self.process.send_signal(2)
        self.read_to_prompt()

def gdb_signals():
    return """
           SIGHUP
           SIGQUIT
           SIGILL
           SIGABRT
           SIGEMT
           SIGFPE
           SIGKILL
           SIGBUS
           SIGSEGV
           SIGSYS
           SIGPIPE
           SIGALRM
           SIGTERM
           SIGURG
           SIGSTOP
           SIGTSTP
           SIGCONT
           SIGCHLD
           SIGTTIN
           SIGTTOU
           SIGIO
           SIGXCPU
           SIGXFSZ
           SIGVTALRM
           SIGPROF
           SIGWINCH
           SIGLOST
           SIGUSR1
           SIGUSR2
           SIGPWR
           SIGPOLL
           SIGWIND
           SIGPHONE
           SIGWAITING
           SIGLWP
           SIGDANGER
           SIGGRANT
           SIGRETRACT
           SIGMSG
           SIGSOUND
           SIGSAK
           SIGPRIO
           SIG33
           SIG34
           SIG35
           SIG36
           SIG37
           SIG38
           SIG39
           SIG40
           SIG41
           SIG42
           SIG43
           SIG44
           SIG45
           SIG46
           SIG47
           SIG48
           SIG49
           SIG50
           SIG51
           SIG52
           SIG53
           SIG54
           SIG55
           SIG56
           SIG57
           SIG58
           SIG59
           SIG60
           SIG61
           SIG62
           SIG63
           SIGCANCEL
           SIG32
           SIG64
           SIG65
           SIG66
           SIG67
           SIG68
           SIG69
           SIG70
           SIG71
           SIG72
           SIG73
           SIG74
           SIG75
           SIG76
           SIG77
           SIG78
           SIG79
           SIG80
           SIG81
           SIG82
           SIG83
           SIG84
           SIG85
           SIG86
           SIG87
           SIG88
           SIG89
           SIG90
           SIG91
           SIG92
           SIG93
           SIG94
           SIG95
           SIG96
           SIG97
           SIG98
           SIG99
           SIG100
           SIG101
           SIG102
           SIG103
           SIG104
           SIG105
           SIG106
           SIG107
           SIG108
           SIG109
           SIG110
           SIG111
           SIG112
           SIG113
           SIG114
           SIG115
           SIG116
           SIG117
           SIG118
           SIG119
           SIG120
           SIG121
           SIG122
           SIG123
           SIG124
           SIG125
           SIG126
           SIG127
           SIGINFO
           EXC_BAD_ACCESS
           EXC_BAD_INSTRUCTION
           EXC_ARITHMETIC
           EXC_EMULATION
           EXC_SOFTWARE
           EXC_BREAKPOINT
           """.split()

