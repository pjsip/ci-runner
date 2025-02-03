import abc
import argparse
import datetime
import glob
import os
import subprocess
import sys
import time
from typing import List


class Runner(abc.ABC):
    '''
    Abstract base class for runner class.
    '''

    TIMEOUT = 3600
    '''Default timeout'''

    def __init__(self, path: str, args: List[str], 
                 timeout: int):
        """
        Parameters:
        path        The path of (PJSIP) program to run
        args        Arguments to be given to the (PJSIP) program
        timeout     Maximum run time in seconds after which program will be killed
                    and dump will be generated
        """
        self.path = os.path.abspath(path)
        '''Path to program'''
        if not os.path.exists(self.path):
            raise Exception(f'Program not found: {self.path}')
        
        self.args = args
        '''Arguments for the program'''

        self.timeout = timeout
        '''Maximum running time (secs) before we kill the program'''

        self.popen : subprocess.Popen = None
        '''Popen object when running the program, will be set later'''

        self.info(f'running. cmd="{self.path}", args={self.args}, timeout={self.timeout}')

    @classmethod
    def info(cls, msg, box=False):
        t = datetime.datetime.now()
        if box:
            print('\n' + '#'*60)
            print('##')
        print(('## ' if box else '') + t.strftime('%H:%M:%S') + ' cirunner: ' + msg)
        if box:
            print('##')
            print('#'*60)
        sys.stdout.flush()

    @classmethod
    def err(cls, msg, box=False):
        t = datetime.datetime.now()
        if box:
            sys.stderr.write('\n' + '#'*60 + '\n')
            sys.stderr.write('##\n')
        sys.stderr.write(('## ' if box else '') + t.strftime('%H:%M:%S') + 'cirunner: ' + msg + '\n')
        if box:
            sys.stderr.write('##\n')
            sys.stderr.write('#'*60 + '\n')
        sys.stderr.flush()
        
    @classmethod
    @abc.abstractmethod
    def get_dump_dir(cls) -> str:
        """
        Returns directory where dump file will be saved
        """
        pass

    @abc.abstractmethod
    def get_dump_path(self) -> str:
        """
        Get the path of core dump file
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_dump_pattern(cls) -> str:
        """
        Get file pattern to find dump files
        """
        pass

    @classmethod
    @abc.abstractmethod
    def install(cls):
        """
        Install crash handler for this machine
        """
        pass

    def detect_crash(self) -> bool:
        """
        Determine whether process has crashed or just exited normally.
        Returns True if it had crashed.
        """
        dump_path = self.get_dump_path()
        return os.path.exists(dump_path)

    @abc.abstractmethod
    def process_crash(self):
        """
        Process dump file.
        """
        pass

    @abc.abstractmethod
    def terminate(self):
        """
        Terminate a process and generate dump file
        """
        pass

    def warmup(self):
        """
        This will be called before run()
        """
        pass

    def run(self):
        """
        Run the program, monitor dump file when crash happens, and terminate
        the program if it runs for longer than permitted.
        """
        self.warmup()
        self.popen = subprocess.Popen([self.path] + self.args, bufsize=0)
        self.info(f'program launched, pid={self.popen.pid}')
        
        try:
            self.popen.wait(self.timeout)
        except subprocess.TimeoutExpired as e:
            self.info('Execution timeout, terminating process..', box=True)
            self.terminate()
            time.sleep(1)
            if not self.popen.returncode:
                self.popen.returncode = 1234567

        if self.popen.returncode != 0:
            self.info(f'exit code {self.popen.returncode}, waiting until crash dump is written')
            for _ in range(60):
                if self.detect_crash():
                    break
                time.sleep(1)

            if not self.detect_crash():
                self.err('ERROR: UNABLE TO FIND CRASH DUMP FILE!')
                dump_dir = self.get_dump_dir()
                pat = self.get_dump_pattern()
                files = glob.glob(os.path.join(dump_dir, pat))
                self.err(f'ls {dump_dir}/{pat}: ' + '  '.join(files[:20]))
            else:
                self.info(f'crash dump found: {self.get_dump_path()}')
                time.sleep(5)

        if self.detect_crash():
            self.info('Processing crash info..', box=True)
            self.process_crash()

        # Propagate program's return code as our return code
        self.info(f'Exiting with exit code {self.popen.returncode}')
        sys.exit(self.popen.returncode)



def main(cls: Runner):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--install', action='store_true',
                        help='Install crash handler on this machine')
    parser.add_argument('-t', '--timeout', type=int,
                        default=Runner.TIMEOUT,
                        help='Max running time in seconds before terminated')
    parser.add_argument('prog', help='Program to run', nargs='?')
    parser.add_argument('args', nargs='*',
                        help='Arguments for the program (use -- to separate from cirunner\'s arguments)')

    args = parser.parse_args()

    kwargs = {}
    if args.timeout is not None:
        kwargs['timeout'] = args.timeout

    if args.install:
        cls.install()

    if args.prog:
        ci_runner = cls(args.prog, args.args, **kwargs)
        ci_runner.run()
        # will not reach here
