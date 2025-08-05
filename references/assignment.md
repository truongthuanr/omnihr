# Backend Assignment #2

This is a technical assignment for the scope of senior backend engineer

# Overview

The task is to write a simple **django** / **fast-api** microservice for an HR company . You would be responsible for building the API that populates the employee search directory .

![Screenshot 2023-10-27 at 8.12.57 PM.png](./assignment1.webp)

Feel free to create entities and their attributes as you like in the relational DB .   

> 💡 Only the search API has to be implemented . Please ignore the `Add employee` `Import` `Export` CTA

> 💡 You are only required to implement the search API . You do not have to implement crud API for any of the entities

The following are the filter options of the API .

![Screenshot 2023-10-27 at 8.44.39 PM.png](./assignment2.webp)

The following are the responsibilities of the search API 

### Dynamic columns :

Different organisations will love to have different columns in the output , while the above example displays `contact info` `department` `location` `position` . Some organizations would love to display the `department` `location` `position` columns only . So you can assume the order , the columns are configurable at an organization level .

> 💡 you do not have to create crud api to store the configuration of columns for the organizations . Assume it’s stored in configuration of your choice ( DB / file / etc )

### Performance :

Please assume that there are millions of users in the database , so do design the API considering the heavy load that could be placed on the API ( after sharding etc )

### Rate-limitting

We do not want users abusing the API , so please create an appropriate rate-limiting system as possible to prevent the user from spamming the API

# Deliverables

**The following are things to include in your submission**:

- Link to your Github repository containing all code and toolings needed to install and run your CLI tool
- A `README.md` file containing anything you think is important to know **for a potential end-user** (likely a fellow developer). Assume use of a unix environment (mac/linux)

**The following are functional requirements**

- The service must be containerized .
- The API information must be sharable in an **OPEN API** format
- The API must be unit tested
- No external library is allowed for rate-limitting . Please your own implementation no matter how naive it is .
- There shouldn’t be a data leak in the API such ( information of other organisation’s  users , extra attributes of user that is not displayed on the UI etc ) .
- The assignment must be in python / fast API

> 💡 there is no need to create the relations in migration etc . Please stick to focusing as much time on the API as possible

**The following are the non-functional requirements**:

- You may not use any external dependencies or libraries (only standard library is allowed)
- You may use external testing libraries if you choose to write tests
- The application should execute correctly in a Linux (or UNIX-like) environment

# Final notes

If we find your submission of sufficient quality, we will have a further discussion on your code architecture as well as pair to modify your code to simulate a real-world situation where stakeholders will require constant change/feature upgrades. So don't copy and paste too much
