# Bugs 

The aim of this task was to  find and fix bugs in the code so the website worked as expected.

## How I approached the task

I decided to approch this task by doing manual testing. I started by testing on an admin acccount as that type of account would have more functionality, then go on to test my fixes also worked on normal user accounts. 

## Findings

### Donor Wall

#### Problem
Clicking onto this page immediately gave a Django template syntax error "Invalid block tag on line 32"

#### Exploration:
I could see from the error message provided by Django that the prolem was coming from the donor_wall.html template on line 32, it also suggested that the issue might have been a forgotten `endfor` tag. I separated    the if and for loops onto different lines to closer mirror Python syntax and also make it easier to see what I was dealing with 

#### Solution: 
In separating the tags this problem went away and also made the code easier to read so I could see that the for loop and if statement had been closed and closed in the correct order. 

#### Follow up testing done: 
Now the page was rendering properly I clicked all through the pages using the number buttons and the next/previous buttons to check the pagination worked correctly and it rendered different data on each page. I also made donations in different names to ensure that data was pulling through properly, which it was. However adding no name to the pledge left the donor wall looking odd.

#### Problem:
No name in the pledgee field gives no default "anonymous" in the name, it just leaves a blank and then says donated X amount which did not look right.

#### Exploration: 
Does this need to be dealt with in the model or the template? I looked at removing `blank=True` from this field in the `ProjectPledge` model and set a default value to "anonymous". However this has the potential to introduce other issues, so I then looked at fixing this problem in the template.

#### Solution:
Add an if statement to the donor wall template. So if there is a name in the pledgee field show that, else (so if it's blank) put "Anonymous" in as the name. 


### Projects Page

#### Problem: 
When a pledge is made it shows up on the Donor Wall but does not appear to increase the total on the project list page. 

#### Exploration
In order to fix this problem I first needed to work out what was being called, from where and what it was trying to do. In doing this I found out that this functionality uses the fragment (as an include in the `project_detail.html` page), this form then calls the `PledgeView`. Now that I had located the code in question, I did some rubber duck debugging, and read through each line of the function seeing what it did and what I thought it should be doing. Once I thought I understood what the code was doing I put in various print statements to see what parts of the code were being hit and in what order. From this I could see that it was adding the correct amount (which made sense as it was showing up on the donor wall and none of the error conditions were met). I then realised that the donations were getting added but with a long delay (about 5 minutes or so). Now I had decided that there was no issue with that view I then looked elsewhere for where this issue could be coming from. From here I then looked at where/when the data was being pulled for the list view. 

#### Solution: 
After more print statements to see how/when code was being hit I saw that this data was being cached and not cleared when it was updated. As this is a value that would change a lot and made it look to users that their donation hadn't been added, I removed all of the cache functions to force it to pull the data again so it was always up to date. By doing this if you made a donation and then headed straight back to the projects list you could see the total would reflect the most recent addition. 

#### Further testing: 
Now that the values were updating I tested what would happen if anything other than a number or a "." was added to the amount field. It wouldn't let me add letters or any symbol that wasn't a decimal point, and even if I managed to get a character in, when I hit the pledge button it would highlight the error and not let me proceed. 

#### Problem:
Can make a negative donation and it takes money away from the total raised for that project. 

#### Exploration: 
I started with the `ProjectPledge` model as this is where things such as type is set for each field. There was no minimum value set for the amount field, thus allowing the negative amounts to be donated. 

#### Solution:
Import the `MinValueValidator` for Django and add `validators=[MinValueValidator(0)]` to the amount so that it would not accept values less than 0.


### Leaderboard

#### Problem:
The leaderboard by amount table was rendering the wrong way with the lowest values at the top, as opposed to the leaderboard by donor table which was listing the houses with the highest value at the top.

#### Exploration:
In the LeaderboardView the count was rendering largest to smallest for the leaderboard by donor table and I saw the “-“ in the `.order_by()` so looked up reverse order and that backed up my thought that that was the difference between the correct order and incorrect order. 

#### Solution: 
Add a “-“ to `order_by(“amount_sum”)` for the leaderboard by amount table.

#### Further testing:
Checked the number of donations per house and amount donated by that house updated after a donation was made. I then made a donation with no house assigned to see what it did.

#### Problem:
No other/anonymous rendered with the houses if a donation is made but not assigned to a house it just renders another row with nothing where the house should be.

#### Exploration: 
I decided this should be fixed in the template as not to end up offering “Anonymous” as a house option.

#### Solution: 
Add if statements in template so if `row.house_choices == “”` it renders "Anonymous" else it renders `row.house_choices`.

#### Further testing:
Add more donations against no house and see if it adds to the "Anonymous" row or adds more rows. Adding additional rows for each anonymous would be a bug, but as designed, it added to the same row rather than create more rows for each unassigned donation.


### My Profile

#### Problem:
Updating name does not change name on the Donor Wall for future donations.

#### Exploration: 
I looked to the pledge form as that’s where the data for the donor wall is created and added a print statement to see if `self.request.user.name` (educated guess) would return what I expected, the name assigned to the account, which it did.

#### Solution: 
Change the `initial_data` value to have `.name` at the end. However this then left the field blank for users who have not set a name. So I then adjusted this to first check if `self.request.user.name` else use `self.request.user` to provide the email address in the pledgee field.

## Normal user testing: 
Having done all the testing and bug fixes on an admin account I then repeated the tests on a normal user account and did not encounter any further bugs or issues on this account type. 

## Other tests considered

After manual testing and flushing out the bugs that way I would then look at automated testing using something like PyTest or another testing frame work used elsewhere across solutions provided by the company to help maintain proper working functionality as things are added and changed on the site moving forward. 

[Back](README.md)