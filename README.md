# Expense_app
Clone of split wise for tracking group expenses


# To run The project

1) Make sure you have python installed. (python3.8)
2) Afterwards create a virtual environment by using package venv
   "python3.8 -m venv myenv"
3) Activate the virtual environment
   "source myenv/bin/activate" on mac & linux
   "myvenv\Scripts\activate" on windows

4) Now Install the Requirements
   "pip install -r requirements.txt"

5) After Installing requirements, create and run the migrations
   go to root of project (./manage.py is located there)
   "./manage.py makemigrations"
   "./manage.py migrate"

6) Finally, you can run the project locally by using :-
   "./manage.py runserver"

# Note:- To Figure out payload for the APIS, please look at the test cases in Each App
   
