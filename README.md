# MLBstats
An exercise in GUI building and web scraping. Script opens a navigable GUI that is used to download 2016 season data from baseballreference.com and displays the data in a table.

please note that brscaper.py was taken from: https://github.com/andrewblim/br-scraper
I only made small adjustments to account for the basereference's updated html formatting. 

dependencies: beautifulsoup4, pyqt5, also written in python3.

MLBstats launches a GUI. From there the user can press the download button to initiate the fetching of data. Once data is downloaded, type in any name into the search bar (automated sugggestions will help you find the guy you're looking for) and then click "add player" to load that player into the table.

So far the GUI only supports data for the 2016 season, and only for hitter. Will be updated soon to expand data capabilities. 
