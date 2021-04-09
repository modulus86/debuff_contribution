## README

This is a script designed to figure out how much `Mystic Touch` and `Chaos Brand` add to a persons damage / DPS. Currently this is done purely by pulling the damage from a WCL repo, breaking down a player's damage into Magical and Physical damage, then dividing by 1.05. The assumption is that if the corresponding class is in the raid then the debuff is up 100% of the time on every mob - obviously this isn't accurate in a real-world scenario, as such this will ONLY give a maximal possible contribution and in real terms will be much less. This could be used to determine if the damage added by bringing a Monk or DH outweights bringing something that does more damage.
 
## Requirements 

* Python 3.6+
* Requests 
* WCL account with an API key

## Installation

Running the command `pip install requirements.txt` in the root directory of the project will install all of the requirements.

## Usage

You should be able to run this with the command:
`python debuff.py <WCL API v1 key> <WCL report>`

## Feedback 

This is a work in progress, so and feedback is welcome. I don't expect this to be of a huge use to people and was more created out discussions with my guild and if bringing a WW monk would be worth it for the debuff or if the player should just play something else that does more damage. [note: this was before it was determined that WW was actually good damage]
