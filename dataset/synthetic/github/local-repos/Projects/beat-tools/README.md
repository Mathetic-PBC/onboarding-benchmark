# beat-tools

Small scripts for my FL Studio / sample library setup.

- `docs/library-layout.md`: where things live
- `flp_backup.sh`: weekly zip of FL Studio projects
- `list_samples.py`: samples per pack and kind
- `beat_tools/rename.py`: normalize sample names to `<kind>_<descriptor>_<nn>[_<key>][_<bpm>].wav` (dry run by default, `--apply`, `--undo` from `rename_log.csv`)
- `beat_tools/bpm.py`: tempo estimate for loops without a BPM in the name (`rename.py --detect-bpm`)
