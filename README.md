# Hubbub Codetest project

## Running under Docker

    $ docker-compose up --build

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ docker-compose run --rm django python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

#### Running tests with pytest

    $ docker-compose run --rm django pytest

### Bugs

[Here](bugs.md) are the bugs encountered during this challenge and how they were resolved.

### Imporvements

On top of fixing the bugs I felt that some other improvments needed to be made to help better the user experience. Deatils of these improvements can be found [here.](improvements.md)