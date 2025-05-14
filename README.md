# Energy Engineering Simulation Lab

# Advanced Computational Lab in Energy Engineering

## Setup
### Install `miniconda`

Miniconda is a minimal version of `Anaconda`, a popular open-source platform for managing Python environments and packages. Unlike the full [Anaconda distribution](https://www.anaconda.com/download/), which includes numerous pre-installed scientific Python libraries and tools (such as NumPy, Pandas, Matplotlib, Jupyter, and more), Miniconda contains only the essentials: the conda package and environment manager as well as Python.

With Miniconda you can:
- Create and manage Python environments: You can install multiple versions of Python and switch between them, which is particularly useful when different projects require different Python versions.
- Install packages: Since conda is a cross-platform package manager, you can install packages tailored specifically for your environment and platform.
- Use less storage space: Miniconda is significantly smaller than Anaconda, as it only contains a basic installation that you can expand with specific packages as needed.

You can always add extra packages via `conda install packagename`, and Miniconda will automatically install all necessary dependencies.

Visit the [Miniconda installation page](https://docs.conda.io/en/latest/miniconda.html). You can also quickly install Miniconda [via the command line](https://docs.anaconda.com/miniconda/#quick-command-line-install).

### Managing environments with `conda`

Using Python with a package manager allows you to create isolated, reproducible _environments_ in which you have full control over all installed packages and configurations.

First, check if you have access to `conda` in your _terminal_ (if possible) or the _Anaconda Prompt_ (common on Windows) by typing:

    conda --version

Then make sure your conda installation is up to date:

    conda update -n base -c conda-forge conda

### Environment for this course

The current environment specifications for this course can be found in this [`YAML` file](https://en.wikipedia.org/wiki/YAML): `environment.yaml`

After navigating to the directory where the file `environment.yaml` is stored ([here](https://tutorials.codebar.io/command-line/introduction/tutorial.html) is a tutorial on how to navigate using the command line), you can create the environment using `conda`:

    conda env create -f environment.yaml

Activate this environment:

    conda activate simlab-env

This environment should be sufficient for all tasks in this course.

You are now ready to run your simulations in TESPy or EbsilonProfessional!

## Additional Information
### General information about `conda`

To create a conda environment, run the following command:

    conda create --name my_environment python=3.12 numpy

To use this environment, simply activate it by typing:

    conda activate my_environment

You should now see the string `my_environment` in your prompt.
From now on, every Python execution will use the packages installed in your `my_environment` environment.

To install additional packages in your environment:

    conda install <package_name>

Some packages are maintained by the community (e.g., `conda-forge`) and require you to specify a different "channel":

    conda install -c conda-forge <package_name>

You can deactivate your environment by entering:

    conda deactivate

To list all environments on your system:

    conda env list

For a full overview of all packages installed in your environment, run:

    conda list

If you want to permanently delete an environment and remove all associated data:

    conda env remove --name my_environment --all

A conda environment can also be defined via an `environment.yaml` file. This file allows you to recreate an environment with the exact same configuration by running:

    conda env create -f my_environment.yml

For comprehensive documentation on using environments, see the
[conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html).

### Markdown

During the course, you will write texts in Markdown format. This is also widely used in Jupyter. [Here](https://www.markdownguide.org/basic-syntax) you can find a guide on the basic syntax of Markdown.
