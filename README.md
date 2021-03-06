# trello-cli

This is a very simple Python3 module for communicating with the Trello API. It
comes with a small command line tool which allows you to list boards, lists and
cards. You can create new cards with labels, a comment and a description.

## Installation

Build and install the Debian package:

```
dpkg-buildpackage -rfakeroot -b -us -uc

cd ..

sudo dpkg -i python3-trello-cli_0.1.0-1_all.deb
```

## CLI Usage

Create a configuration file `~/.trello-cli/config.json` and set your app key and
token like this:

```json
{
    "key": "xxxxxxxxxxxxxxxxx",
    "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

List all your boards:

```sh
$ trello-cli list boards
|   0 | 5aef57cf5878e2223de3d796 | Spare                                    |
|   1 | 5aeddc7238bfa37f65227ba1 | TestBoard                                |
```

List all columns in a board:

```sh
$ trello-cli list lists --board-id="5aeddc7238bfa37f65227ba1"
|   0 | 5aee01947afe7dd2dc784df8 | List1                                    |
|   1 | 5aee01979779eb62491ffdcf | List2                                    |
```

List all labels in a board:

```sh
$ trello-cli list labels --board-id="5aeddc7238bfa37f65227ba1"
|   0 | 5aee2a9703e80b77e7c11f84 |                             | green      |
|   1 | 5aee2aa15ace49e909fde207 | Bla                         | orange     |
```

List all cards in a list:

```sh
$ trello-cli list cards --list-id="5aee01947afe7dd2dc784df8"
|   0 | 5af0b5e2fc54c15b9ff1d34e | Card 1                                   |
```

Create a new card in a list:

```sh
$ trello-cli create card \
    --list-id="5aee01947afe7dd2dc784df8" \
    --name="Card 1" \
    --desc="Card description" \
    --labels="5aee2a9703e80b77e7c11f84,5aee2aa15ace49e909fde207" \
    --comment="This is a comment!" \
    --due="31 May 2020" \
    --position 0
```

The `--position` parameter determines, where a card is going to be inserted. Say
`0` to insert the card at the beginning of the list, omit `--position`
altogether to append the card to the list. Choose `1` to insert the card after
the first element. Choose `2` to insert the card after the 2nd element. Choose
`-1` to insert the card before the last element. And so on..

Move a card to another list:

```sh
$ trello-cli move card --card-id="5af410338d1e01ded11cf268" \
    --list-id="5af40e5df0cb48ff44e15fb0"
```

Delete a card:

```sh
$ trello-cli delete card --card-id="5af1fd058a39ae3e3e8b74d1"
```

## API Usage

Before doing anything else, you need to initialize the Trello client context:

```python
from de.tobijk.trello import Client as TrelloClient

TrelloClient("###MY_APP_KEY###", "###MY_TOKEN###")
```

You can now go ahead and work with Trello boards, lists and cards.

```python
from de.tobijk.trello import Board

my_boards = Board.all()

for board in my_boards:
    print(board.id, board.name)
```

Once you know the identifier of a board, you can query it for lists (columns):

```python
from de.tobijk.trello import Board

board = Board.by_id("5aeddc7238bfa37f65227ba1")

lists = board.lists()

for l in lists:
  print(l.id, l.name)
```

And once you know the identifier of a list, you can query it for cards:

```python
from de.tobijk.trello import List

list_ = List.by_id("5aee01947afe7dd2dc784df8")

cards = list_.cards()

for c in cards:
    print(c.id, c.name, c.desc)
```

To create a new card, you need a list identifier and a card object:

```python
from de.tobijk.trello import List, Card

list_ = List.by_id("5aee01947afe7dd2dc784df8")

card = Card()

card.name     = "Card Name"
card.desc     = "Card Description"
card.idLabels = ["labelId1", "labelId2"]
card.due      = "31 May 2020"

list_.insert(0, card)
```

The `insert` method behaves like python list's `insert` method with respect to the insert position.

In order to add a comment to a card:

```python
card.add_comment("This is a comment.")
```

Move a card to another list:

```sh
Card({"id": "5af1fd058a39ae3e3e8b74d1"}).move_to("5aee01947afe7dd2dc784df8")
```

In order to delete a card:

```python
Card({"id": "5af1fd058a39ae3e3e8b74d1"}).delete()
```

