# ByteBlogger API Documentation

# Endpoints
API Endpoints

Here are the available API endpoints you can interact with:

    User Signup

    Endpoint: http://localhost:8080/signup-email
    Method: POST
    Description: Register a new user with an email and password.
    Parameters: JSON payload with email and password.
    User Login

    Endpoint: http://localhost:8080/login-email
    Method: POST
    Description: Authenticate a user using their email and password.
    Parameters: JSON payload with email and password.
    Get All Posts

    Endpoint: http://localhost:8080/posts
    Method: GET
    Description: Retrieve all blog posts.
    Get Post by ID, Update, and Delete

    Endpoint: http://localhost:8080/posts/<post_id>
    Methods: GET, PUT, DELETE
    Description:
    GET: Retrieve a blog post by its ID.
    PUT: Update a blog post by its ID.
    DELETE: Delete a blog post by its ID.
    Get Posts by User

    Endpoint: http://localhost:8080/posts/user/<username>
    Method: GET
    Description: Retrieve blog posts by a specific user.
    Like/Unlike a Post

    Endpoint: http://localhost:8080/posts/<post_id>/like/<user>
    Methods: POST, DELETE
    Description:
    POST: Add a like to a blog post.
    DELETE: Remove a like from a blog post.
    Create a Comment

    Endpoint: http://localhost:8080/posts/<post_id>/create-comment
    Method: POST
    Description: Create a comment for a specific blog post.
    Parameters: JSON payload with user and content.

# Docker
The ByteBlogger API is containerized and available on DockerHub for easy deployment.

### DockerHub Repository

You can find the containerized application on DockerHub via the following link: [ByteBlogger DockerHub Repository](https://hub.docker.com/repository/docker/ethanqg/flask-byteblogger/general)

### Running the Container

Frontend developers can run the API as a container and make HTTP requests to access API data. Follow these steps to get started:

1. **Pull the Docker Image**: Pull the Docker image from the DockerHub repository using the following command:

   ```bash
   docker pull ethanqg/flask-byteblogger:v1.0

2. Run the container:
    docker container run -p 8080:8080 ethanqg/flask-byteblogger-2:v1.2

3. Make HTTP requests:
    fetch('{{ insert endpoint here }}')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Handle the data returned by the API
    console.log(data);
  })
  .catch(error => {
    // Handle errors, e.g., network issues or API errors
    console.error('There was a problem with the fetch operation:', error);
  });
