# CitationUtil

Small utility scripts to access citation service.

Currently there are two scripts:
- getJSON.py: Download JSON file for specified MIP, institute, model and experiment.
- addExperiments.py: Modify MIP-granuality JSON file to experiment-granuality JSON file.
- modCreators.py: Replace Creators section.
- postJSON.py: Post JSON file.
- checkCiteComplete.py: Check the completion of the data reference information

All of these use an API provided by the citation service, and it is
necessary to login the service to access this API.  So these scripts
may be useful for only the Citation manager in each modeling team.

# Requirements
- python 3.6.7 (maybe ok for other version)

# License
BSD-3-Clause.
