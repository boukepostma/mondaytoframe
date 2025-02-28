release_patch:
	uv run bump2version patch
	git push --tags

release_minor:
	uv run bump2version minor
	git push --tags

release_major:
	uv run bump2version major
	git push --tags
