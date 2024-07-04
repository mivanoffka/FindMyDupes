# **What is FindMyDupes?**

FindMyDupes is a simple python application that helps you search for duplicate images. You may find it useful to prepare datasets for machine learning.

The app is crossplatform for all major dekstop systems ans can be launched on Windows, GNU/Linux and MacOS.

Moreover, you are able to use _FindMyDupes Internal Server_ in case you want to integrate it with your project. It is not necessary to launch the GUI of the app.

At last, FindMyDupes is easy to extend. You may implement any ways of searching besides the built-in method of _perceptual hash comparison._

# **How do I launch FindMyDupes?**

First of all, obviously, clone the repository to your local machine

```bash
git clone https://github.com/mivanoffka/FindMyDupes
```

If you don't have git installed, you are always able to just download the project archive from here.

FindMyDupes requires Python 3.10+. You may use your global interpreter, yet it is better create a local virtual environment in order to avoid library conflicts.

```bash
cd path\to\project
python -m venv .venv
```
Before launching the project and setting its libraries, you ought to activate the virtual environment.

On Windows:

```bash
.venv\Scripts\activate
```

On UNIX systems (MacOS included):

```bash
source .venv\bin\activate
```

Python libs required to launch FindMyDupes are listed in _requirements.txt_. You don't have to install each of them manually, just use

```bash
pip install -r requirements.txt
```

Now the project is ready and you may launch the app 

```bash
python main.py
```



























 
