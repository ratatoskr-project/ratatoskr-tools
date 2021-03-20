# ratatoskr-tools
ratatoskr-tools is an API that helps the user to automate the simulation of ratatoskr simulator. Moreover, it also provides the API that visualized the NoC network traffic heat.

## Installation
1. Clone this repository to any folder that you would like to work for. (For example ~/Documents/ or ~/).
> $ git clone https://github.com/jmjos/ratatoskr-tools.git

2. Create virtual environment to install this package in it and activate the virtual environment. The provided Makefile has provided the packages for the virtual envoronment. If you want to install in your machine locally, then skip this step.
> $ make

> $ source source_me.sh

3. Install this package to your current working environment. (If your environment exists python and python3 then use python3 instead of python).
> $ python setup.py install

## API Tutorials
- [tutorial 1: Overall simulation](./tutorials/tutorial1.md)
- [tutorial 2: ratatoskr GUI client](./tutorials/tutorial2.md)
- [tutorial 3: Bandwidth single simulation](./tutorials/tutorial3.md)

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details