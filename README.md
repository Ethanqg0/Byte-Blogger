# Blogging API

# Concerns
    #1: Is the API currently stateless? 
    #2: gitignore currently does not work
    #3: Performance? Wanted to add caching but was not sure because the data keeps being updated from new threads.

# DOCUMENTATION
    # not done yet

# Folder Organization: 
    Microservices architecture. The authentication, services, and data modificaiton are loosely coupled and heavily modularized. 
    Blueprints to modularize app instances

# Consisten Data Format: JSON/ JWT
    Only uses JSON formatting and JSON web tokens in responses
    Extremely simple, also assisted with the help of Supabase

# Increased Performance: Caching
    Introduced Caching use MemCache in Flask
    Utilized manual testing files with 100 compared rates
    Utilized automated testing from Postman
    Significant increase in performance from caching. First response time compared to the average of the other 99 improved by 40%
    Uses memoization, a programming topic that is now being applied to real applications

# Long-term outlook: Versioning
    Not done

    Introduced versioning in API routes with version numbers to ensure that future upgraded versions in dependencies will not conflict with API