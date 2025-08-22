# DQN from Scratch in C

This repository contains a complete implementation of a Deep Q-Network (DQN) reinforcement learning algorithm from scratch in pure C, with no external dependencies. The project includes a custom implementation of the CartPole environment, neural network architecture, matrix operations, and visualisation capabilities.

![CartPole Demo](example.gif)

## Project Overview

The entire project was built from the ground up to test and strengthen my proficiency in deep learning algorithms and reinforcement learning concepts.

## Features Implemented

### Deep Learning Components
- **Neural Network Framework**: Complete feedforward neural network with customisable layers
- **Matrix Operations**: Matrix operations
- **Activation Functions**: ReLU implementation
- **Loss Functions**: Huber loss
- **Adam Optimizer**: Advanced adaptive optimisation algorithm

### Reinforcement Learning Components
- **Experience Replay Buffer**: Stores and samples past experiences
- **Target Network**: Stabilises learning by slowly updating target Q-values
- **Epsilon-Greedy Policy**: Balances exploration and exploitation
- **Q-Learning**: Implements discounted rewards for long-term planning

### Environment and Visualization
- **CartPole Environment**: Classic control problem implementation
- **Simple Graphics System**: Visualises the CartPole state
- **Video Recording**: Capability to save agent episodes as Y4M videos

## Compiling and Execution

This project uses no third-party libraries, so all you need is a GCC compiler.

To compile the project, run the following command from the project root:

```bash
gcc -Iinclude train.c src/*.c -o train -lm
```

To run the program after compilation:

```bash
./train
```

When you run the program, it will:
1. Initialise the neural network and environment
2. Train the DQN agent for a specified number of steps
3. Record 3 episodes of the trained agent
4. Save the recordings as Y4M video files

## Customisation

You can adjust the training parameters in `train.c`, including:
- Learning rate
- Epsilon decay rate (controls exploration vs. exploitation)
- Discount factor
- Network architecture
- Number of training steps
- Batch size
- Experience replay buffer size

Feel free to experiment with different parameters to optimise training for the CartPole task.

## Contact

If you have any questions about this project or are interested in discussing deep learning research opportunities, academic collaborations, or potential roles please reach out to me at tristanjlegg@gmail.com.

This project demonstrates my deep understanding of neural networks and reinforcement learning by implementing everything from scratch with no dependencies.

# Minecraft Style Stable Diffusion

This repository contains a complete implementation of a LoRA fine-tuning system for Stable Diffusion 1.5, trained to generate images in a Minecraft visual style. The project includes tools for both training custom LoRA weights and inferring images using pre-trained weights.

## Examples

Below are examples showing the difference between the base Stable Diffusion 1.5 model and the same model with the Minecraft LoRA adapter applied. Both images were generated with the same prompt "A cabin in the woods" and the same seed (0) for direct comparison:

### Base SD 1.5 Output
![Base SD 1.5 output](assets/base.png)

### Minecraft LoRA Applied
![Minecraft LoRA applied](assets/lora.png)

## Project Overview

The Minecraft Style Stable Diffusion project allows you to generate Minecraft-like images from text prompts. It works by applying a LoRA adapter to the base Stable Diffusion 1.5 model, which shifts the model's output toward a Minecraft aesthetic without changing the base model itself.

## Features

- **Pre-trained Minecraft LoRA**: Use the pre-trained LoRA weights from Hugging Face (TristanJLegg/MinecraftStyleStableDiffusion)
- **Custom Training**: Train your own LoRA weights using the provided training script
- **Inference Tool**: Generate Minecraft-style images from text prompts
- **Custom Dataset**: Uses the TristanJLegg/MinecraftGameplayCaptioned dataset created specifically for this project

## Getting Started

### Prerequisites

This project was tested using Python 3.10.14. It's recommended to install packages in this order:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

pip install -r requirements.txt
```

### Generating Images with Pre-trained Weights

To generate images using the pre-trained Minecraft LoRA weights:

```bash
python infer.py "A cabin in the woods"
```

By default, this will pull the Minecraft LoRA weights from Hugging Face and apply them to Stable Diffusion 1.5.

#### Additional Options

Use the `--help` flag to see all available options:

```bash
python infer.py --help
```

Parameters:
- `--lora_weights`: Specify a different LoRA weights path or Hugging Face repo
- `--output_file`: Custom filename for the output image
- `--seed`: Set a specific seed for reproducible generation

### Training Your Own LoRA

To train your own Minecraft LoRA adapter:

```bash
python train.py
```

This will train a LoRA adapter using the TristanJLegg/MinecraftGameplayCaptioned dataset, which contains Minecraft gameplay screenshots paired with descriptive captions.

#### Customising Training

Use the `--help` flag to see all available training options:

```bash
python train.py --help
```

Parameters:
- `--weights_name`: Custom filename for the output weights
- `--lora_rank`: Rank of the LoRA adapter
- `--lr`: Learning rate
- `--resolution`: Image resolution for training
- `--max_train_steps`: Maximum number of training steps
- `--batch_size`: Batch size for training

## Contact

If you have any questions about this project or are interested in discussing deep learning research opportunities, academic collaborations, or potential roles please reach out to me at tristanjlegg@gmail.com.

## Acknowledgments

- This project uses the Stable Diffusion model by Runway
- The Minecraft dataset was created by gathering and captioning gameplay screenshots

# ExplorationAgent

## Models

This "main" branch contains the implementations of the GRU and non-sequential models of this work. Swap to the "transformer" branch to use the transformer architecture.

## Installation

These instructions were tested using a bash terminal in Ubuntu 22.04.4 LTS.

Clone this repository to your development folder and navigate in:
```bash
git clone https://github.com/TristanJLegg/ExplorationAgent.git &&
cd ExplorationAgent
```

A [Miniconda](https://docs.anaconda.com/miniconda/install/) environment is created and activated with Python 3.10.14 to manage our packages:
```bash
conda create -n ExplorationAgent python=3.10.14 &&
conda activate ExplorationAgent
```

Install the required pip packages:
```bash
pip install -r requirements.txt
```

## Scripts

*All scripts must be run from within the repository directory*.

Edit the config.yaml to change the training, environment and output parameters.

To start training run:
```bash
python train.py configs/train_gru_config.yaml
```
This will create a training tensorboard in the 'runs' directory.

To evaluate the trained agent run:
```bash
python evaluate.py configs/evaluate_gru_config.yaml
```
This will create a tensorboard in the 'runs' directory that will store the results of 10 environments running in parallel.

To take a video of the agent playing the environment run:
```bash
python video.py configs/video_gru_config.yaml
```
This will create a video of an environment episode in the 'videos' directory.

To play and test the environment yourself run:
```bash
python play_world.py
```

## Troubleshooting

Ensure these system packages are installed on your system:
```bash
apt install libgl1-mesa-glx libglu1-mesa libglfw3-dev libgles2-mesa-dev libfreetype6 libfreetype6-dev
```

Ensure these conda packages are installed in your Miniconda environment:
```bash
conda install -c conda-forge libstdcxx-ng
```
