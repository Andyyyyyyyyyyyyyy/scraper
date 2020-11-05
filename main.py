import configparser
import praw
import scraper
import re
import csv

config = configparser.ConfigParser()
config.read("config.ini")

reddit = praw.Reddit(client_id=config.get("ACCOUNT", "CLIENT_ID"),
                     client_secret=config.get("ACCOUNT", "CLIENT_SECRET"),
                     username=config.get("ACCOUNT", "USERNAME"),
                     password=config.get("ACCOUNT", "PASSWORD"),
                     user_agent="HeadlineScraping, created by u/ItsTheRedditPolice")

subreddit = config.get("SUBREDDIT", "NAME")

user = reddit.user.me()

domain_list = []

def extract_domain(string):
    # This will extract domain from a url (e.g. https://www.google.com will become google.com
    # this is so i can compare with domains in domains.csv
    regex = r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)"
    url = re.findall(regex,string)
    return [x for x in url]

def load_db(): # this will load domains.csv into domain_list
    with open("domains.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            str = "".join(row)
            domain_list.append(str)

def scan_submissions():
    try:
        for submission in reddit.subreddit(subreddit).stream.submissions(skip_existing=True):
            if not submission.is_self:
                link = submission.url
                link_domain = extract_domain(link)[0]
                for domain in domain_list:
                    if domain == link_domain:
                        title = submission.title
                        domain_name = link_domain.split(".")[0]
                        headline = getattr(scraper, domain_name)(link) # call a function using a variable name "getattr(module, varname)(args)"
                        # TODO: compare submission titles to headline and do the most appropriate action
                        if headline != title:
                            comment = submission.reply("Hey, your submission has been removed! \n\n "
                                             "Reason: \n\n "
                                             "```Submission Title does not match the one in the article you "
                                                   "linked to!``` \n\n Please repost your submission and be sure to make the title "
                                                   "the **exact same** as the headline in the article! Thank you! \n\n ^^I ^^am ^^a ^^bot")
                            comment.mod.distinguish(how="yes", sticky=True)
                            submission.mod.remove(spam=False, mod_note="Title did not match headline.")
    except Exception as e:
        print(f"** ERROR: {e}")

def initialise():
    load_db()
    scan_submissions()


initialise()