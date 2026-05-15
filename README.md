# So, what is this?

This is a tool I made, that I thought of making when myself and a friend were working on a project involving an FPGA.

We were sending code snippets, whole infra changes, etc. over WhatsApp texts - using zip files, pasting code directly into chats, and so on. It was very messy.

I had a pretty simple idea:
make something like a git server, and when you push code into it (or upon some other event), the server triggers another system, which then pulls the latest code, builds it, and flashes the board.

The idea started when we were developing FPGA code - synthesising it, implementing it, and then flashing the bitstream (using open-source toolchains like yosys, nextpnr, etc). This is also applicable for MCUs as well - I used a simple blinky code for an STM board as an example while developing this tool.

So, if there is an available toolchain on Linux, it should still work the same way, pretty much.

# Specifics

Instead of a separate machine running the git server, I ran all of this inside Podman containers.

The project currently works using two containers:

* one contains the toolchain required to build/synthesise/etc.
* the other contains the Gitea server.

Why Gitea?

Well, eventually maybe one would want to use GitHub for the webhook that triggers the whole "pull latest code and build it" flow - and you absolutely can.

Gitea looks a lot like GitHub, so in future it should absolutely be possible to replace the Gitea container with GitHub webhooks instead.

But then you'd have to set up IPs, routing, and where exactly the webhook should point. In a local environment, Gitea still feels like a pretty good idea.

For now, the Gitea webhook is received by a Flask application.

A simple POST route is defined, which when triggered, runs a command using subprocesses - it tells Podman to run the toolchain container and build the newer code.

This can be done in a few ways:

* either write a script that handles the whole build/synthesis/flash flow
* or use the container workspace directly and run bash commands there

The first option sounds better imo, but you do you.

# To reproduce the results

Get the code for your board ready first.

Make sure it works normally first - as in, do all the steps manually first, the same way you would normally work with the board/toolchain. This is mostly for your own sanity.

Then put that script into `webhook_server.py` - so whenever the Flask server is triggered (like from the webhook), your script runs, and the container works with the newer code.

Edit `compose.yaml` as needed, since my folder structure and yours will probably be different.

Run:

```bash
podman-compose up
```

Then go to:

```text
http://localhost:3000
```

(or some other port, depending on what you configured while setting up Gitea)

You should see the Gitea page there.

Setup Gitea - leave most things as default, just set the SSH port to `2222` (it will probably be `22` initially).

After that, write a script for your board flashing/build process.

Run the Python Flask server.

Then put:

```text
http://host.containers.internal:5000/flash
```

into the webhook Target URL.

HTTP method should be:

* POST

Trigger should be:

* Push Events

To test it:
click on "Test Push Event".

The history under the button should show a green tick, and your board should get flashed as expected.

# A few things

This is a very basic automation flow. Nothing special, but I think it will be immensely useful and convenient when working in groups.

I also plan to eventually deploy this onto a Raspberry Pi and connect boards directly to its USB ports.

This project is still pretty rough around the edges, but the main workflow does work.
