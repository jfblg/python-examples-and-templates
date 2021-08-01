import os
import subprocess
from time import time

def start_1_subprocess():
    proc = subprocess.Popen(['echo', 'Hello from the child'], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    print(out.decode('UTF-8'))


def start_and_wait_for_subprocess():
    proc = subprocess.Popen(['sleep', '0.2'])
    while proc.poll() is None:
        print("Working...")
    print("Exit status ", proc.poll())


def run_sleep(period):
    return subprocess.Popen(['sleep', str(period)])


def start_multiple_subprocesses():
    start = time()
    procs = []
    for _ in range(10):
        proc = run_sleep(0.1)
        procs.append(proc)

    for proc in procs:
        proc.communicate()

    end = time()
    print("Finished in %.3f seconds." % (end - start))


def run_openssl(data):
    env = os.environ.copy()
    env["password"] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(['openssl', 'enc', '-des', '-pass', 'env:password'],
    env=env,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc


def run_md5(input_stdin):
    return subprocess.Popen(
        ['md5'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)


def start_multi_openssl():
    input_procs = []
    hash_procs = []
    for _ in range(3):
        data = os.urandom(10)
        p = run_openssl(data)
        input_procs.append(p)
        hash_proc = run_md5(p.stdout)
        hash_procs.append(hash_proc)

    for p in input_procs:
        p.communicate()
    for p in hash_proc:
        out, err = p.communicate()
        print(out.strip())


def use_timeout():
    proc = run_sleep(10)
    try:
        proc.communicate(timeout=0.1)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait()

    print("Exit status: ", proc.poll())

def main():
    # start_multi_openssl()
    use_timeout()


if __name__ == "__main__":
    main()
