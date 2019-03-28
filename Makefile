pull_2018_data:
	wget -r --no-parent -i data_urls.txt

install_requirements:
	pip install -r requirements.txt