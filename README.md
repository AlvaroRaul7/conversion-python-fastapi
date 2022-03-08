# Documentation Low Level Problem

`cd conversion-api`

** If you want to run the app without docker **

First, install the library requirements 

Inside conversion-api folder, run:

`pip install -R requirements.txt`

Inside app folder:
Run:

`uvicorn main:app --reload`

Then, open http://127.0.0.1:8000/docs to see how to use the API


## Docker style

`cd conversion-api`

Build the image:

`docker build --no-cache -t conversion-api .`

Run the image:

`docker run -d -p 4300:80 conversion-api  `


## Rate Limit

The api root `/` has a rate limit of 10 requests per user/day  handled by a log file, because FastAPI doesn't support this feature.

## Security

Security was implemented through JWT tokens from a fake db hard-coded. The username is **johndoe** and the password is **secret**

## How to use

After going to the docs path, there is a Button that says authorize
- Click on it
- Enter username: johndoe
- Enter password: secret
- Leave the rest fields in blank
- Click on authorize

Now you can use the API normally.


## Tests

Recommended: Python 3.7

Inside the app folder:
 
Run:

`pip install pytest`

If your local computer has python3 :

    `python3 -m pytest`
else:
  
  `python -m pytest`

## Deployment

Deployed in AWS EC2 like a docker container:

Open:

http://35.172.227.213:4300/docs

## Future considerations

Implementes Redis as a db to improve scalabilty of the API to handle rate limits and users.




# High Level Problem

Please outline, in as much detail as you can the types of tests you would run, how you would run these tests in a live production environment, and how you would accomplish running these tests given you have live 3rd party integrations.

## Unit Tests

The microservices of the backend application would need unit tests to validate that the service is working properly.
They can use PyTest, Cucumber or several libraries depending on the framework and the language

## Integration Tests

These tests are critically important when deploying multiple microservices. The team can design theses tests using Cerberos for Python to validate the responses between services. To run it automatically you can build a pipeline in Jenkins to run the integration tests before a deploy.

## User Testing

Last but not least, the user expects the system to work normally, so in case the system has a frontend. Test all the paths and functionalities exhaustively.

# Scenario Problem

How do you handle this situation?

- First set up 2 different meetings: One with my team and the other one with the E2 Developer

- Talk to my team first to let them know that everything is going to be fine, and we are going to build a better process for the mock services to speed up development.

Anticipated response:

The team is not happy and they want me to be mean with the other E2 Developer.

- Talk to the E2 Developer to let him know the problems that we are facing an build a protocol together to have the latest mock available in order to reduce incidents.

Anticipated response:

The E2 Developer doesnt recognize his fault because he is too proud.

