# CitationUtil
Small utility scripts to access citation service.

Currently there are two scripts:
- updateCitation.py: Submit CMIP6 Citation info of experiment granularity.
- checkCiteComplete.py: Check the completion of the data reference information

Both use the APIs provided by the citation service. Especially ``updateCitation.py`` needs to login the service, so this may be not useful except for the Citation manager in each modeling team.

# Requirements
- python 3.6.7 (maybe ok for other version)

# License
BSD-3-Clause.
