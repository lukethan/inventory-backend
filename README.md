# Keg South Inventory Webapp Backend
"inventory-backend" is a Flask application hosted on PythonAnywhere that provides information to a React frontend via RESTful APIs.

## Relevant Links
  * [Public-Facing Website](https://lukethan.github.io/inventory/)

  * [Front-End Repository](https://github.com/lukethan/inventory)

### Client Needs:
  * Inventory management system that can be accessed via the internet, and updated by a number of different employees

  * CRUD capabilities for adding new items, updating existing ones, as well as deletion of old products

  * Daily snapshots of total inventory at closing time

### Application Breakdown
  * In order to meet the client's needs, I decided to link a Flask application with a PythonAnywhere PostgreSQL database.
    I considered using FastAPI because my main goal was to design RESTful APIs that interacted with a simple database schema, but
    PythonAnywhere only allows for WSGI hosting at the moment. Designing API routes for the create, read, update, and delete functions
    was relatively simple, but I had to add a separate route for photos that can be uploaded to the frontend. The upload API downloads
    the photograph into a static directory in my backend and then generates and stores a URL in the database so that the photo can be
    served to the frontend. Daily snapshots occur via PythonAnywhere's scheduled tasks and involve a SQL dump.

##### To create your own backend on PythonAnywhere:
  1. Create an account on PythonAnywhere
  2. Click on the 'database' tab and create a database
  3. Clone the repository using the bash console on PythonAnywhere
  4. Due to many dependencies being provided by PythonAnywhere, I would recommend downloading dependencies one at a time\*\*
  5. Create a .env file at the same directory level as the application and add relevant information for the database connection
  6. Initilize the database for the first time using the class created in the python script. (PythonAnywhere has a good tutorial)
  7. Test out the database by using Postman website to send requests or by opening a MySQL console and manually adding items
  8. Visiting your website should display JSON formatted items in your database
  9. Congrats! You can start designing your frontend or use the repo here as inspiration: [Front-End Repository](https://github.com/lukethan/inventory)

  \*\*A requirements.txt has been included to mass download dependencies but create a virtual environment before doing this to avoid 
  duplicate dependencies between the PythonAywhere local directory and your project .local directory.
