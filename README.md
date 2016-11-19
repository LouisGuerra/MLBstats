# MLBstats
An exercise in GUI building and web scraping. Script opens a navigable GUI that is used to download 2016 season data from baseballreference.com and displays the data in a table.

please note that brscaper.py was taken from: https://github.com/andrewblim/br-scraper
I only made small adjustments to account for the basereference's updated html formatting. 

dependencies: beautifulsoup4, pyqt5, also written in python3.


How it works:
MLBstats launches a GUI. From there the user can press the download button to initiate the fetching of data. Data is fetched by calling a method in brscraper.py that visits a team page and returns a dictionary for the data within that page's table. This method is repeated once for each team. These tables are consolidated and formatted into a single dictionary. Care is taken to make sure that averages (batting average and on-base percentage) across different teams are calculated properly for each player. 

Once data is downloaded, you can type in any name into the search bar (automated sugggestions will help you find the guy you're looking for) and then click "add player" to load that player into the table.

So far the GUI only supports data for the 2016 season, and only for hitters. The code will be updated soon to expand data capabilities. 
