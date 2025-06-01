import random
from datetime import datetime

story_templates = [
    """I used to lose money every weekend chasing wins on FanDuel. Parlays, bad beats, emotional picks — you name it. After years of frustration, I realized it wasn’t *betting* that I loved — it was the **competition**.

That’s why I built **Sure-Odds** — a completely free sports challenge that rewards **streaks**, not stakes.

No money down. No gambling. Just picks. Every day, you get a new shot to build a streak and win real cash prizes (up to $500/week).

It’s like fantasy meets sports betting — but zero risk.

Would love for you to try it and tell me what you think:
👉 https://sure-odds.com/

And yeah, if you're tired of losing dumb bets, this might be the cure.
""",
    """I hate how betting makes every loss feel personal. Even when the pick is right, the odds can still burn you.

So I built something different.

**Sure-Odds** is a free challenge where every correct pick builds your streak — and your streak can win you real cash.

There’s no money involved. Just sports IQ. $500 every week, up for grabs.

It’s not a sportsbook. It’s not betting. It's skill-based, daily sports competition.

Join if you’ve ever thought, “I’d win more if it wasn’t about the juice.”
👉 https://sure-odds.com/
""",
    """I’ve lost too many parlays to count. One leg away. Always.

That’s why I stopped betting, and built **Sure-Odds** instead — a free streak challenge where you prove you know sports, without losing a cent.

Each pick you get right grows your streak. Biggest streaks win the weekly pot — up to $500.

There’s no betting. Just picking.

It’s part fantasy, part leaderboard, all pride.

Try it here: https://sure-odds.com/

And let me know what you think — feedback from real bettors means everything.
"""
]

def generate_reddit_story():
    post = random.choice(story_templates)
    print("📢 Reddit Story Post:\n\n" + post)

generate_reddit_story()
