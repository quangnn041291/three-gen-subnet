<div align="center">

# **THREE GEN | TEST SUBNET 89**

[![Discord Chat](https://img.shields.io/discord/308323056592486420.svg)](https://discord.gg/bittensor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

</div>

3D generation subnet provides a platform to democratize 3D content creation, ultimately allowing anyone to create virtual worlds, games and AR/VR/XR experiences. This subnet leverages the existing fragmented and diverse landscape of Open Source 3D generative models ranging from Gaussian Splatting, Neural Radiance Fields, 3D Diffusion Models and Point-Cloud approaches to facilitate innovation - ideal for decentralized incentive-based networks via Bittensor. This subnet aims to kickstart the next revolution in gaming around AI native games, ultimately leveraging the broader Bittensor ecosystem to facilitate experiences in which assets, voice and sound are all generated at runtime. This would effectively allow a creative individual without any coding or game-dev experience to simply describe the game they want to create and have it manifested before them in real time.

---
## Project Structure

The project is divided into three key modules, each designed to perform specific tasks within our 3D content generation and validation framework:

- Mining Module(`mining`): Central to 3D content creation, compatible with miner neurons but can also be used independently for development and testing.

- Neurons Module (`neurons`): This module contains the neuron entrypoints for miners and validators. Miners call the RPC endpoints in the `mining` module to generate images. Validators retrieve and validate generated images. This module handles running the Bittensor subnet protocols and workflows.

- Validation Module (`validation`): Dedicated to ensuring the quality and integrity of 3D content. Like the mining module, it is designed for tandem operation with validator neurons or standalone use for thorough testing and quality checks.

## Hardware Requirements

Pending detailed benchmark results (see TODOs), our recommended setup aligns with Google Cloud's a2-highgpu-1g specs:
- GPU: NVIDIA A100 40GB
- CPU: 12 vCPUs
- RAM: 85GB
- Storage: 200GB SSD
Expectations under continuous operation include about 500GB/month in network traffic and 0.2MB/s throughput.

## OS Requirements

Our code is compatible across various operating systems, yet it has undergone most of its testing on Debian 11, Ubuntu 20 and Arch Linux. The most rigorous testing environment used is the Deep Learning VM Image, which includes pre-installed ML frameworks and tools essential for development.

## Setup Guidelines for Miners and Validators

### Environment Management With Conda

For optimal environment setup:
- Prefer [Conda](https://docs.conda.io/en/latest/) for handling dependencies and isolating environments. It’s straightforward and efficient for project setup.
- If Conda isn’t viable, fallback to manual installations guided by `conda_env_*.yml` files for package details, and use `requirements.txt`. Utilizing a virtual environment is highly advised for dependency management.

### Process Supervision With PM2

To manage application processes:
- Adopt [PM2](https://pm2.io) for benefits like auto-restarts, load balancing, and detailed monitoring. Setup scripts provide PM2 configuration templates for initial use. Modify these templates according to your setup needs before starting your processes.
- If PM2 is incompatible with your setup, but you're using [Conda](https://docs.conda.io/en/latest/), remember to activate the Conda environment first or specify the correct Python interpreter before executing any scripts.

## Running the Miner

To operate the miner, the miner neuron and generation endpoints must be initiated. While currently supporting a single generation endpoint, future updates are intended to allow a miner to utilize multiple generation endpoints simultaneously.

### Generation Endpoints

#### Setup
Set up the environment by navigating to the directory and running the setup script:
```commandline
cd three-gen-subnet/generation
chmod +x setup_env.sh
./setup_env.sh
```
This script creates a Conda environment `three-gen-mining`, installs dependencies, and sets up a PM2 configuration file (`generation.config.js`).

#### Running
After optional modifications to generation.config.js, initiate it using [PM2](https://pm2.io):
```commandline
pm2 start generation.config.js
```

#### Validation
To verify the endpoint's functionality for video generation:
```commandline
curl -d "prompt=pink bicycle" -X POST http://127.0.0.1:8093/generate_video/ > video.mp4
```
For testing 3D object generation: http://127.0.0.1:8093/generate.

#### Miner Neuron

#### Prerequisites

Ensure wallet registration as per the [official bittensor guide](https://docs.bittensor.com/subnets/register-validate-mine).

#### Setup
Prepare the neuron by executing the setup script in the `neurons` directory:
```commandline
cd three-gen-subnet/neurons
chmod +x setup_env.sh
./setup_env.sh
```
This script generates a Conda environment `three-gen-neurons`, installs required dependencies, and prepares `miner.config.js` for PM2 configuration.

#### Running
Customize `miner.config.js` with wallet information and ports, then execute with [PM2](https://pm2.io):
```commandline
pm2 start miner.config.js
```

#### Monitoring Miner Activity
Validators update the miner every 20 minutes. It's normal not to observe requests in the initial hour. Absence of requests beyond this period suggests an issue, often due to network inaccessibility. Verify accessibility using:
```commandline
nc -vz [Your Miner IP] [Port]
```

## Validator

To operate the validator, the validator neuron and validation endpoints must be initiated. 

### Validation Endpoint

#### Setup
Set up the environment by navigating to the directory and running the setup script:
```commandline
cd three-gen-subnet/validation
chmod +x setup_env.sh
./setup_env.sh
```
This script creates a Conda environment `three-gen-validation`, installs dependencies, and sets up a PM2 configuration file (`validation.config.js`).

#### Running
After optional modifications to validation.config.js, initiate it using [PM2](https://pm2.io):
```commandline
pm2 start validation.config.js
```

#### Validator Neuron

#### Prerequisites

Ensure wallet registration as per the [official bittensor guide](https://docs.bittensor.com/subnets/register-validate-mine).

#### Setup
Prepare the neuron by executing the setup script in the `neurons` directory:
```commandline
cd three-gen-subnet/neurons
chmod +x setup_env.sh
./setup_env.sh
```
This script generates a Conda environment `three-gen-neurons`, installs required dependencies, and prepares `validator.config.js` for PM2 configuration.

#### Running
Customize `validator.config.js` with wallet information and ports, then execute with [PM2](https://pm2.io):
```commandline
pm2 start validator.config.js
```

### Autoupdater
