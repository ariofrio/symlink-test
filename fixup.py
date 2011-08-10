import os
import subprocess
import optparse

parser = optparse.OptionParser(
    usage='%prog [OPTIONS]',
    description='Setup symlinks on Windows (not needed no Mac or Linux)')

parser.add_option(
    '-n', '--simulate',
    action='store_true',
    help="Do not actually create the symlinks")

parser.add_option(
    '--git-cmd', metavar="COMMAND_NAME",
    default="git.cmd",
    help="Name of the git command (default: git.cmd)")


def main():
    options, args = parser.parse_args()
    proc = subprocess.Popen([options.git_cmd, 'ls-files', '-s'], stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    lines = stdout.splitlines()
    for line in lines:
        parts = line.split()
        if parts[0] == '120000':
            fn = parts[3]
            fn = fn.replace('/', '\\')
            symlink(fn, options.simulate, options.git_cmd)

def symlink(fn, simulate, git_cmd):
    if os.path.exists(fn):
        print 'File already exists; assuming symlink okay:'
        print '  %s' % fn
        return
    proc = subprocess.Popen([git_cmd, 'checkout', fn])
    proc.communicate()
    fp = open(fn)
    name = fp.read().strip()
    name = name.replace('/', '\\')
    fp.close()
    os.unlink(fn)
    if not simulate:
        # This is so bizarre...
        print 'Symlinking %s to %s' % (fn, name)
        proc = subprocess.Popen(['cmd', '/c', 'mklink', os.path.basename(fn), name], cwd=os.path.dirname(fn) or '.', shell=True)
        proc.communicate()
        if proc.returncode:
            print 'Command failed; maybe you need to run as administrator?'
 
if __name__ == '__main__':
    main()
