from __future__ import print_function
import subprocess
import os
import sys
import shutil
import datetime
import distutils.dir_util

if sys.version_info < (3,):
    input = raw_input
    str = unicode

pwd = os.getcwd()

appver_file = r'.\AppVer'

target_shares = {
    'release': [],
    'test'   : [],
    'dev'    : []
    }
# it needs this transformation because msbuild does a direct string concatenation instead of a path join.
target_shares = {k: [p if p.endswith(os.path.sep) else p+os.path.sep for p in v] for k, v in target_shares.items()}

output_dir = r'bin\publish'
publish_dir = r'bin\publishapp.publish'
msbuild_folder = r'%ProgramFiles%\MSBuild\12.0\bin\amd64' \
                 if os.path.exists(r'%s\MSBuild\12.0\bin\amd64' % os.environ['PROGRAMFILES'])\
                 else r'%ProgramFiles(x86)%\MSBuild\12.0\bin\amd64'


def get_appver():
    with open(appver_file) as fd:
        return fd.readline().strip()

def incr_appver(ver):
    vers = ver.split('.')
    vers[-1] = str(int(vers[-1]) + 1)
    return '.'.join(vers)

def set_appver(ver):
    with open(appver_file, 'w') as fd:
        fd.write(ver)

def get_cmd(target, ver, env):
    template = r'"{0}\msbuild" /t:clean;publish /property:OutputPath={1},PublishUrl={2},InstallUrl={2},UpdateUrl={2},ApplicationVersion={3},MinimumRequiredVersion={3},AssemblyName="{4}"'
    cmd = template.format(msbuild_folder, output_dir, target, ver, 'NST System Configurator '+env)
    return cmd

if __name__=='__main__':
    error = {}
    print('current python implementation version is', sys.version)
    print('currently working in: %s' % pwd)
    print('please make sure this script runs directly under the project folder.')
    env = input('build environment(%s): ' % ', '.join(sorted(target_shares.keys())))
    while env not in target_shares:
        print("nonexisting environment: {}".format(env), file=sys.stderr)
        env = input('build environment(%s): ' % ', '.join(sorted(target_shares.keys())))

    ver = incr_appver(get_appver())
    for i, p in enumerate(target_shares[env]):
        cmd = get_cmd(p, ver, env+str(i))

        print('executing {}'.format(cmd))
        print('----------------------------------')
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        with proc.stdout:
            for l in proc.stdout:
                print(l.strip().decode('utf-8'))
        proc.terminate()
        print('----------------------------------')

        if proc.returncode == 0:
            try:
                distutils.dir_util.copy_tree(publish_dir, p)                
            except Exception as e:
                error[p] = e
                sys.stderr.write("error occurred: %s\n" % str(e))
                distutils.dir_util.copy_tree(publish_dir, r'bin\backup' + '\\' + str(i))
        else:
            print("error: %d" % proc.returncode, file=sys.stderr)
        print

    if len(error) != 0:
        print('Error occurred:', file=sys.stderr)
        for k, e in error.items():
            print('%s: %s\n' % (k, str(e)), file=sys.stderr)
        print('has backed up the folder.', file=sys.stderr)

    try:
        set_appver(ver)
    except IOError as e:
        print("failed to write to file: %s" % str(e), file=sys.stderr)
        print('next application version will be %s.' % incr_appver(ver), file=sys.stderr)

    input('press enter to continue...')
