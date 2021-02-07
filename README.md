# Installation Guide
## Without Docker
1. Install Python3.8 or higher
2. Install PostgreSQL 12
3. Install Dependencies
	```bash
	sudo apt-get  update  && apt-get  install  -y  \
	software-properties-common  gdal-bin  libgdal-dev  g++  git  \
	python3-dev  libpng-dev  zlib1g-dev
	```
4. Clone Repository
5. Create Virtual Environtment
	```bash
	python3.8 -m venv venv
	```
		
6. Activate Virtual Environtment
	```bash
	source venv/bin/activate
	```
7. Install Requirements
	```bash
	pip install -r requirements.txt
	```
8. Adjust value like database settings etc at file `project/settings.py`
9. Run Migrate
	```bash
	./manage.py migrate
	``` 
10. Run app
	```bash
	./manage.py runserver
	``` 
11. Open `localhost:8000/docs` to show api documentation

## With Dokcer
```bash
docker-compose up
```

## Analysis
1. Describe what you think happened that caused those bad reviews during our 12.12 event and why it happened
    - Based on the cases described above. In my opinion, the causes of out stock are as follows:
        1. stock that does not differentiate between non flash sale products and flash sale products
        2. Lack of validation at checkout.
        3. No control over the actual stock.
        4. The time limit for payment between flash sale and non-flash sale is too long
2. Based on your analysis, propose a solution that will prevent the incidents from occurring again
    - My solution is:
        1. differentiate stock for flash sale and non flash sale products.
        2. Set limit payment time
        3. Monitoring stock