# Dectblproc

Dectblproc is a decision table-based testing application which provides an algorithm to solve given table and determine inconsistent and redundant pairs. It also checks the rules whether if they are satisfiable or not. Then it creates test suites for satisfiable rules. 

## Getting Started

In the beginning, you need to setup your environment to be ready for running the codes. Also you can find more information about Decision Table-Based Testing in "documentation.pdf".


### Prerequisites

There some prereqisites for this project, respectively:
- Python
- MiniSAT

This project was developey via python. To be able to build and run it, your system needs to have python. If you do not have, installation is straightforward. You can follow the installation processes from "python.org" depends on your operating system.
Python 3 is highly recommended for you as a version.
If you have "pip" in your system, you can install python easily with this command

```
pip install python3
```

Another prereqisite is MiniSAT. MiniSAT, is a sat solver which provides to solve boolean expressions and gives the values for the variables in the expression. The installation is depens on your operating system.
If your operating system is Windows, you can use cywgin. Installation processes can be followed from here

```
http://web.cecs.pdx.edu/~hook/logicw11/Assignments/MinisatOnWindows.html
```

If you are using MacOS or Linux, installation is straightforward.
"Homebrew" may be used for MacOS and "Linuxbrew" may be used for Linux systems.

```
brew install minisat
```

### Installing

Installation of the project is very easy. After you setup your environment (prereqisites), you only need to clone the project. 

The command is

```
git clone https://github.com/omeerkorkmazz/dectblproc.git
```


## Build & Execute

The only path you need to follow to run the project is to open terminal and use python command.
Check the steps respectively.

```
cd <repo-dir>
```

```
python dectblproc.py ~repoPath\dectblproc\Data_Files\datafile_name
sample ==> python dectblproc.py O:\dectblproc\Data_Files\dt0
```

## Built With

* [Python](http://python.org) - The programming language used
* [MiniSAT](https://minisat.se/) - SAT Solver used


## Authors

* **Omer KORKMAZ** - *Owner*


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

