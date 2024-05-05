# NWO Subscriptions

## Overview

This is a simple FastAPI loosely following a three-tiered design pattern: [Read More Here](https://levelup.gitconnected.com/structuring-fastapi-project-using-3-tier-design-pattern-4d2e88a55757)

![Simple diagram of 3-tier design for FastAPI](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*0LlheIYfXsrio2-t.png)

## Explainer

### OAuth2.0

The application leverages the built-in authentication features of FastAPI to provide OAuth2.0. Passwords are hashed/salted using a library called Jose, which provides JWT functionality. When a user logs in, their id, email, admin flag, as well as an expiration timestamp are stored in a token, which is then passed in via the Bearer header on each subsequent request.

#### Admin Role

The app includes a very basic administrator flag, which can be set during user registration. This is necessary to:
- Download a list of all subscriptions
- Create/Edit other users' subscriptions

In addition to these functions, admins can of perform the same functions as a regular user, such as:

- Create subscription for themselves
- Update their existing subscription
- Get their existing subscription

### Data Layer

The data layer uses SQL Alchemy + SQL Alchemy ORM in a Session Factory pattern. This effectively injects/reuses a single instance of Session application-wide. 

### Service/Business Layer

The service layer comprises all services found in /app/services. These serve as a broker between the controllers and the data layer, and will contain any business logic, such as the 1 subscription per user is rule. Alternatively, this could be enforced on the SQL layer via a UNIQUE constraint. Doing it in the Python layer makes it more accessible to developers, but also introduces the possibility of bugs. Doing it on the SQL layer promises to be more robust, but more obfuscated from developers and admins.

### Controller Layer

Controllers are instances of the API router class, and are sorted into the /apps/routes folder. This API uses a skinny controller methodology, having the service layer do most of the heavy lifting of a given request. Controllers merely establish the routing, and pass request data from the client to the service layer, and the response data from the service layer back to the client. Skinny controllers have the advantage of being developer friendly, making adding routes and diagnosing bugs easy.

### Model Validation

Model/DTO validation is provided through pydantic. It applies to all classes in the /app/schema folder, not to the database models themselves. DB model validation is handled by SQL Alchemy, and db models are found in the /app/models folder.

## Alternative Approaches

I looked at other frameworks for accomplishing this task. Pros/cons listed below

### Django REST Framework

Initially, I was excited about using this. I have heard good things about Django, and know it is widely used for applications that have a UI layer. The advantages of using Django would be:

- It is a true framework, providing things like ORM, model validation, authentication out of the box
- Healthy developer community--lots of articles and tutorials, and third-party libaries to use

Disadvantages of using Django:

- Documentation for REST Framework wasn't very good. It failed to establish best practices (such as controller routing) out of the box. There are three ways to do it, and no strong argument for which way is correct.
- Steep learning curve
- Fitting a square peg into a round hole. As Django is not strictly an API Framework, some of its features (such as a baked-in UI) were difficult to turn off/obfuscate. It didn't feel like a true API framework.

### Flask

Additionally, I looked at Flask. Some advantages:

- Good testing framework
- Extendability
- Known to scale better than Django (but not as well as FastAPI)

Disadvantages:

- Single threaded/synchronous, potentially leading to the server getting locked up on certain types of bugs (such as SQL timeouts)
- Like Django, this is very web UI oriented, and not a true API framework

### FastAPI Pros/Cons

FastAPI is a very popular framework, and was ultimately chosen for this project. It has many advantages:

- Quick startup time. The basic API, with authentication features, swagger, etc. can be spun up quite quickly
- Minimalist approach. Keeping controllers skinny and esablishing the design patterns you want to is quite easy with FastAPI
- Known to be highly scalable, especially with async and threading features
- Built-in data validation with Pydantic is very good

Some disadvantages I would call out:

- Not tightly bundled with any SQL provider. The .Net Web API is a great example of an API framework that is tightly coupled with virtually all features you could desire, such as DB/Code-first database migrations, extensive authentication features, data validation built in, fully functional controller objects/decorators, etc. Django does better here, with is built-in Django ORM.
- Scaffolding features aren't amazing. While it is very light on coding, so this doesn't end up being arduous, it would be nice to add controllers, models, etc. via CLI. This helps developers maintain best practices and keeps your project clean
