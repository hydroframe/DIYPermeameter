# DIY Permeameter

## Launching the application
```
# Clone the repository
git clone git@github.com:cabrowne/DIYPermeameter.git

# Create a conda environment to install dependencies for the app
conda create --name DIYPermeameter python=3.8
conda activate DIYPermeameter

# Install app requirements
cd DIYPermeameter/
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Launching the application with Docker
```
# Pull the image
docker pull hydroframe/diypermeameter:latest

# Launch the image on port 8000
# Dockerfile must be edited to use a different port
docker run -p 8000:8000 hydroframe/diypermeameter:latest
```