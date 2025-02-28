## Motivation
For those looking to adopt a pet, it can be tedious work to look through adoption availability at different animal hospitals. This data visualization app allows users to look at pet avaialbility by age at different animal hospitals, while applying filters such as whether pets have health issues, the type of animal to adopt, and whether a pet is already in adoption process, hence might not be available for adoption.

## App description
A [video description](https://github.com/UBC-MDS/DSCI-532-pet-adoption/blob/main/img/demo.mp4) is inside `img` folder which can also be found [here](https://www.dropbox.com/scl/fi/8kls3k9527hagl5aurehb/demo.mp4?rlkey=39k3y9yu9wmh15urvc28btcek&st=60gjhjn3&dl=0).

## Install instructions

### Step 1: In your terminal, from project root directory, create conda environment:
```bash
conda env create --file environment.yml
```

### Step 2: Activate conda environment:
```bash
conda activate pet
```

### Step 3: Run the app locally:
```bash
cd src
export FLASK_APP=app.py
flask run --host=127.0.0.1 --port=8050
```

### Step 4: To view the app, enter this URL in your web browser address bar:
http://127.0.0.1:8050/
