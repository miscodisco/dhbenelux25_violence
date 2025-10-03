freeform_tags:
	uv run src/save_freeform_tags.py
	
get_genders:
	uv run src/get_relationship_genders.py

assign_violence_cats:
	uv run src/assign_violence_categories.py


preprocess:
	make get_genders
	make assign_violence_cats