#!/bin/bash

podman run -it --rm \
--privileged \
-v $(pwd):/workspace:Z \
stm32-dev \
bash -c "./build-flash.sh"
