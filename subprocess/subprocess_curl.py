import json
import subprocess

from time import time


def run_curl(url):
    proc = subprocess.Popen(['curl', '-X', 'GET', url])
    # proc.stdout(subprocess.PIPE)
    return proc


def process_response(input):
    pass



def get_urls_as_json(urls):
    procs = []

    start = time()

    for u in urls:
        p = run_curl(u)
        procs.append(p)

    for p in procs:
        try:
            out, err = p.communicate(timeout=0.1)
            out_dict = json.loads(out)
            print(out_dict)
        except subprocess.TimeoutExpired:
            p.terminate()
            p.wait()

    print("Finished in %.3f seconds." % time() - start)
        


def main():
    url = "https://jsonplaceholder.typicode.com/posts/"

    urls = [url + str(i) for i in range(10)]
    # get_urls_as_json(urls)
    p = run_curl(url + str(1))
    try:
        out, err = p.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        p.terminate()
        p.wait()

    print("\nOut: {}, Err: {}".format(out, err))


if __name__ == "__main__":
    main()