# Vulture
Created by Ryan '[Ghost](https://github.com/Ghost7926)' Voit and Mark '[Dread](https://github.com/Markofka007)' Perekopsky

This program is built to help automate the task of locating breached credentials on the internet. 
This script currently is built to use Hunter.io and Dehashed APIs to collect infoamtion on a pecified domain or target name. 
In the future, we intend to find and use more APIs to help find and locate more breached credentials. 

This is a work in progress.

Known Error:

Hunter.io rogue '
If there is an ' in a key pair value will breack the JSON formatting, it will break the program. This sometimes occures in the Hunter.io API results, often in the discription of the company. We are working to fix this issue. 
