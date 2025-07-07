# emailgen.py

def generate_email(company, industry, snippet):
    intro = f"""
Hi {company} Team,

I came across your platform and was genuinely impressed by your work in the {industry} space.
"""
    body = f"""
From what I gathered on your website — "{snippet[:200]}..." — it’s clear you're building something meaningful.
At Caprae Capital, we work with growth-stage companies to unlock post-acquisition value through AI-powered strategies and GTM innovation.
"""

    pitch = f"""
Would love to explore how we can partner or support your journey — either through capital, strategic collaboration, or opening new markets.
"""

    close = """
Let me know if you'd be open to a quick intro call. Wishing you continued success!

Warm regards,  
[Your Name]  
Business Analyst Candidate  
Caprae Capital Partners
"""

    return intro + body + pitch + close
