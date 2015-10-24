# API_readings
Web Scraper for Malaysian API and Singapore PSI readings

There are two webscrapers in the this repository.
1. One scrapes data from the Malaysia DOE website, for Malaysia's API readings.(http://apims.doe.gov.my/v2/)
2. One scrapes data from the Singapore National Environment Agencry website for PSI readings on the island. (http://www.haze.gov.sg/haze-updates/historical-psi-readings)

Both scrapers require a database to operate, and currently require a MYSQL DB, but you can easily change this in the db_operations.py script if you wish.

If you're not a techie, the data is capture in a colon,':' delimited file in the ReadingsByRegion(SG&MY) file. 

The full SQL database dump is in the APIScans.zip file.
