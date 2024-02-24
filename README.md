# Test-case-Managements

# some guidlines to start the flask app for test-management cases 

1- create virtual env then install all the lib inside requirements file with the following commands 
       - python -m venv env 
       - pip install -r requirements.txt 

       ##############

2-activate the virtual env  then run the application with with the following command 
        - ./env/scripts/activate
       - python app.py 
       
       ##############

3- after the app is correctly stop the server then run the db__init__.py file to populates the tables in database with test rows
     python  db__init__.py

     ##########

3-then open the postman to login to the app and get access token that required for authentication 
    there are in this repo postman collection with all routes to test their  return results 
    inside the login endpoint change the username and passwoord as you need 
    then enter valid username and password to genrate the valid token (from row that inserted into database in previous command which found in db__init__.py file  )
     
     ################

4- after getting the valid token use it inside postman authorization -> Bearer token 
   then click to do all the crud operations with whatever  http method  

   ###############


5- all the get endpoints has authorization with user to view it only but other operations such as Post  put .delete allow admin only 



