# Using AI Agent to automate recruting process

This process is design to automate the recruting process using AI agents, we have design this project to use minimal cost, this project dosent require any GPU to work on.

The Only things you need to run this project is LLAMA CLOUD API key * and Pinecone API KEY(vector DB).

We are able to build this project in just 8 hour time frame. The future scope of this project can be unimaginable, it can be more scalable and efficient.

### Setting up pinecone 

To set up pinecone, sign up on pinecone and create index with 384 dimensios.(if you're using embedding models of dimensions 384 else adjust accordingly).

# How to run ?!

Firstly change .env file, change the path variable, paste your API KEY's, and your gmail id and gmail id 'APP' password(not gmail passowrd, but gmail id APP password).

## Ingestion

**WARNING - If you're not setting up your own pinecone, please do not run Ingestion pipeline. Jump to Backend..**

If you want to save the data in your OWN VECTOR DB you have to run ingestion pipeline, after setting up the pinecone you have to run main file..

For Now you can use my pinecone.But you have to set the llama cloud API key in .env.

## Backend

To run backend follow this steps..

1) Activate virtual environmen (venv/Scripts/activate) and change paths in .env  according to your system,
2) Move to backend directory
3) run 'uvicorn main:app --reload'

## Frontend

1. to run frontend on streamlit, go to frontend directory
2. and then run 'streamlit run app.py'

Now you're good to go..
