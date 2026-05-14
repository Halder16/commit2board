import subprocess

from flask import Flask, request

app = Flask(__name__)


def run_command(command):
    print(f"Running: {' '.join(command)}", flush=True)
    completed = subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=True,
    )
    if completed.stdout:
        print(completed.stdout, end="", flush=True)
    if completed.stderr:
        print(completed.stderr, end="", flush=True)


@app.post('/flash')
def flash():
    print(
        "Webhook received "
        f"from {request.remote_addr} "
        f"event={request.headers.get('X-Gitea-Event', '-')}",
        flush=True,
    )

    try:
        run_command(["podman", "start", "stm32-dev"])

        run_command([
            "podman",
            "exec",
            "stm32-dev",
            "bash",
            "-c",
            "cd /workspace && ./build-flash.sh",
        ], check=True)

        return "Build and flash successful\n", 200

    except subprocess.CalledProcessError as error:
        print(f"Build/flash failed with exit code {error.returncode}", flush=True)
        if error.stdout:
            print(error.stdout, end="", flush=True)
        if error.stderr:
            print(error.stderr, end="", flush=True)
        return "Build/flash failed\n", 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False)
