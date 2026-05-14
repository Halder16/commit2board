import subprocess

from flask import Flask

app = Flask(__name__)


@app.post('/flash')
def flash():
    print("Webhook received")

    try:
        subprocess.run(["podman", "start", "stm32-dev"], check=True)

        subprocess.run([
            "podman",
            "exec",
            "stm32-dev",
            "bash",
            "-c",
            "cd /workspace && ./build-flash.sh",
        ], check=True)

        return "Build and flash successful\n", 200

    except subprocess.CalledProcessError:
        return "Build/flash failed\n", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
