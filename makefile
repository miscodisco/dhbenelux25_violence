violence_tags:
	python3 src/save_violence_tags.py
	
get_genders:
	python3 src/get_relationship_genders.py

assign_violence_cats:
	python3 src/assign_violence_categories.py


preprocess:
	make get_genders
	make assign_violence_cats