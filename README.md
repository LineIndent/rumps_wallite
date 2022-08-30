# wallite
A macOS menu bar app that stores user debit/credit card number and returns card number copied to clipboard when clicked.


<img width="523" alt="wallite" src="https://user-images.githubusercontent.com/84860195/187414255-cb9190c1-4c0f-41ce-9086-ded5ea095860.png">

How does wallite work?

Wallite simply takes in a user's card number (seperated by spaces) and saves it to a sqlite3 (local) database within the app package contents.
A user enters a card number and wallite checks to see if the card is Visa, MasterCard, or American Express, and subsequently displays the card type and last four digits of the card number. 
Finally, if a card number is clicked, the entire card number, not just the last four digits, are copied to the system clipboard and can be pasted anywhere. 

The following libraries are needed if refinements are to be added separately:
```
pip install git+https://github.com/jaredks/rumps@master   
```
```
pip3 install pyperclip  
```

