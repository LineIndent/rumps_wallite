import sqlite3
import pyperclip
import rumps


class App(rumps.App):
    c = 1

    def __init__(self):
        super(App, self).__init__(name="", icon="./assets/wallet.png")
        self.DisplayWallet()
        self.menu.add(rumps.MenuItem(title="New card", callback=self.ask))

    def DisplayWallet(self):
        db = Database.ConnectDatabase()
        records = Database.ShowTableData(db)
        for data in records:
            self.menu.add(
                rumps.MenuItem(
                    icon=data[1],
                    title="•••• " + data[2],
                    callback=self.copy,
                    key=f"{App.c}",
                ),
            )
            App.c += 1
        db.close()

    def add(self, data, card):
        db = Database.ConnectDatabase()
        TableLength = Database.GetLength(db)
        LastEntry = Database.GetLastMenuItem(db)
        LastEntry = LastEntry[0]

        if TableLength == 1:
            self.menu.insert_before(
                existing_key="New card",
                menuitem=rumps.MenuItem(
                    icon=card,
                    title="•••• " + "{:>}".format(data),
                    callback=self.copy,
                    key=f"{App.c}",
                ),
            )

        else:
            self.menu.insert_after(
                existing_key="•••• " + LastEntry[-4:],
                menuitem=rumps.MenuItem(
                    icon=card,
                    title="•••• " + "{:>}".format(data),
                    callback=self.copy,
                    key=f"{App.c}",
                ),
            )

        App.c += 1

    def copy(self, sender):
        db = Database.ConnectDatabase()
        records = Database.GetCopyNumber(db)
        for number in records:
            number = number[0]
            if number[-4:] == sender.title[-4:]:
                pyperclip.copy(number)
            else:
                pass

    def ask(self, _):
        db = Database.ConnectDatabase()
        win = rumps.Window(
            title="Card Entry Form",
            message="Enter your card number\nUse spaces after every four digit",
            ok="Submit",
            cancel="Cancel",
            dimensions=(175, 23),
        )
        response = win.run()
        string = response.text
        if response.clicked == 1:
            if response.text[0] == "4" and len(response.text) == 19:
                response = response.text[-4:]
                card = "./assets/visa.png"
                values = [string, card, string[-4:]]
                Database.InsertData(db, values)
                self.add(response, card)
                db.commit()
                db.close()
            elif response.text[0] == "5" and len(response.text) == 19:
                response = response.text[-4:]
                card = "./assets/mastercard.png"
                values = [string, card, string[-4:]]
                Database.InsertData(db, values)
                self.add(response, card)
                db.commit()
                db.close()

            elif response.text[0] == "3" and len(response.text) == 19:
                response = response.text[-4:]
                card = "./assets/amex.png"
                values = [string, card, string[-4:]]
                Database.InsertData(db, values)
                self.add(response, card)
                db.commit()
                db.close()
            else:
                rumps.alert(title="Inccorect card number. Try again.")
                self.ask

        else:
            pass


class Database:
    def ConnectDatabase(**kwargs):
        db = sqlite3.connect("wallet.db")
        c = db.cursor()
        c.execute(
            "CREATE TABLE if not exists wallet (CardNumber Text, CardType Text, CardDisplay Text)"
        )
        db.commit()
        return db

    def ShowTableData(db):
        c = db.cursor()
        c.execute("SELECT CardNumber, CardType, CardDisplay from wallet")
        records = c.fetchall()
        return records

    def InsertData(db, value):
        c = db.cursor()
        c.execute("INSERT INTO wallet VALUES (?, ?, ?)", value)
        db.commit()

    def GetCopyNumber(db):
        c = db.cursor()
        c.execute("SELECT CardNumber from wallet")
        records = c.fetchall()
        return records

    def GetLastMenuItem(db):
        c = db.cursor()
        c.execute("SELECT CardNumber from wallet")
        records = c.fetchall()
        if len(records) == 1:
            records = records[-1]
            return records
        else:
            records = records[-2]
            return records

    def GetLength(db):
        c = db.cursor()
        c.execute("SELECT CardNumber from wallet")
        TableLength = len(c.fetchall())
        return TableLength


if __name__ == "__main__":
    app = App()
    app.run()
