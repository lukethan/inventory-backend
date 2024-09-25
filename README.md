# 'Keg South Inventory' Webapp Backend
"inventory-backend" is a Flask application hosted on PythonAnywhere that provides information to a React frontend via RESTful APIs.

### Relevant Links
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

## Inventory API Documentation
### Overview
This RESTful API provides CRUD (Create, Read, Update, Delete) operations for managing product inventory.
### Base URL
`https://kegsouth.pythonanywhere.com`
#### Endpoints
- **URL**: `/`
- **Method**: `GET`
- **Description**: Retrieves a list of products sorted from lowest amount to highest amount.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "item": "Coors Light",
      "amount": 10,
      "imageUrl": "http://example.com/image.jpg"
    },
    "..."
  ]
- **Method**: `POST`
- **URL**: `/`
- **Description**: Adds item and amount to the database.
- **Body**
  ```json
  {
    "item" : "Yeungling",
    "amount" : 2
  }
- **Response**:
  ```json
  {
    "message": "New inventory item added with ID: 93",
    "item": {
        "id": 93,
        "item": "Yeungling",
        "image": "",
        "amount": 2
  }
 - **Error**:
   ```json
   {
    "message": "Item already exists or other error"
   }
- **Method**: `PUT`
- **URL**: `/`
- **Description**: Updates item amount in the database.
- **Body**
  ```json
  {
    "item" : "Yeungling",
    "amount" : 5
  }
- **Response**:
  ```json
  {
    "message": "Yeungling updated!",
  }
 - **Error**:
   ```json
   {
    "message": "Item already exists or other error"
   }
- **Method**: `DELETE`
- **Description**: Deletes item from the database.
- **URL**: `/<item>`
- **Request**: `https://kegsouth.pythonanywhere.com/Yeungling`
- **Response**:
  ```json
  {
    "message": "Yeungling updated!",
  }
 - **Error**:
   ```json
   {
    "message": "Item doesn't exist or other error"
   }
## Image Upload API Documentation
### Overview
This RESTful API stores a user-specified image in the backend then generates and stores a URL in the database to serve the frontend.
### Base URL
`https://kegsouth.pythonanywhere.com`
#### Endpoints
- **URL**: `/upload`
- **Method**: `POST`
- **Description**: Stores image file, generates URL, and stores URL in database to serve '/' GET request
- **Response**:
  ```json
    {
     "message": "File uploaded successfully",
     "imageUrl": "image_url"
    }
- **List of Errors**:
  ```json
    {
     "error": "No file part",
     "error": "No selected file",
     "error": "Invalid item ID",
     "error": "Item not found",
    }
 1. when no image is selected by user
 2. when image filename is empty
 3. when item associated with image doesn't exist
 4. when item associated with image has been deleted
   


## To create your own backend on PythonAnywhere:
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
