# Drylands Radio

A shuffle jukebox that streams the Drylands songs directly from Suno, with live mood buttons.
Nothing is downloaded or rehosted: each track plays from `https://cdn1.suno.ai/<song-id>.mp3`.

Live at: https://aburkum.github.io/jukebox/drylands-radio/

## Updating the catalog
1. Export the catalog CSV (same columns as `catalog.csv`) and replace `catalog.csv`.
2. Run `python3 tools/suno_csv_to_tracks.py drylands-radio/catalog.csv drylands-radio/tracks.json`
3. Commit and push. Mood buttons are generated from the "Mood Tags" column.

Songs must be public (or at least shareable) on Suno for the CDN to serve them.
