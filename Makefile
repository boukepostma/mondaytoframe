model:
	uv run datamodel-codegen \
	--url https://api.monday.com/v2/get_schema?format=sdl \
	--input-file-type graphql \
	--output src/mondaytoframe/model.py \
	--output-model-type pydantic_v2.BaseModel \
	--use-double-quotes \
	--force-optional \
	--target-python-version 3.12