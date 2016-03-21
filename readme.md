# Expert System Creation Engine

Expert System Creation Engine is a project designed to support creation of expert systems based on perceptron approach. The systems should be designed to take *user* input and infer the most fitting object to the clustering problem set by an *expert*. The expert creates a set of logic entities to solve the problem for any possible user input. Main entities of the system are:
  - Objects -- main classification (clustering) entities
  - Attributes -- features that objects possess. Main clustering entity
  - Parameters -- features that are deducted about user data from user input
  - Questions -- interface for user interaction with the system 
  - Answers -- either preset of free-input fields for collecting user input
  - Rules -- logic relations that are used to connect attributes and parameters and also tailor the upcoming questions according to previous answers

Used technologies:
- Backend:
    - Python (Django)
    - MySQL
- Frontend:
    - HTML5
    - JavaScript (JQuery)
    - Twitter Bootstrap
