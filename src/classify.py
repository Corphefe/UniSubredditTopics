from google import genai
import argparse
import time

client = genai.Client()

prompt_template = """
You are an annotation model part of a larger data science project. Your task is to classify a university subreddit post title into ONE of the following 7 categories. 
Read the category definitions carefully and return ONLY the category name — nothing else.

------------------------------
CATEGORIES
------------------------------

1. Course
Definition: Questions or discussions about a specific course or specific professor.
Use When: A course number, course name, or professor implies a specific course.
Do Not Use When: The question is general academics or program-level.
Edge Case: Specific course mentioned but framed as general academic concern.

2. Admissions
Definition: Topics related to university applications and prospective students.
Use When: Application materials, requirements, prospective student questions.
Do Not Use When: General academic concerns or non-admissions student topics.
Edge Case: Scholarships for incoming students count as Admissions.

3. Academic
Definition: General academic topics for current students not tied to a specific course.
Use When: GPA, registration, policies, programs, exchange.
Do Not Use When: Specific course mentioned → Course. Application context → Admissions.

4. Leisure & Lifestyle
Definition: Activities done for enjoyment: socializing, fitness, eating out, dating, fashion.
Use When: Clubs, gyms, food, campus hangouts, fun activities.
Do Not Use When: Academic, work, or practical life tasks.
Edge Case: Pastimes related to academics/work fall under those categories.

5. Life & Resources
Definition: Practical logistics outside school and work: housing, furniture, healthcare, pets, theft, transportation, finances.
Use When: Living, daily needs, practical problems.
Do Not Use When: Fun activities (→ Leisure), work (→ Work), academics.
Edge Case: Posts mixing many topics (grades + rent + loneliness) may fit here.

6. Current Events & Activism
Definition: News, politics, university policy, activism, referendums.
Use When: Newsworthy events, political actions, administrative updates.
Do Not Use When: Personal life questions, clubs, or student-run events.
Edge Case: University governance (SSMU, admin decisions) can count here.

7. Work & Research
Definition: Internships, jobs, part-time work, professional development, research roles.
Use When: Any paid work, career preparation, job search, research assistant roles.
Do Not Use When: Academic coursework, leisure, or personal life topics.
Edge Case: Academic references made only in service of career goals → Work.

------------------------------
INSTRUCTIONS
------------------------------
• Classify the following Reddit POST TITLE.
• Choose EXACTLY ONE category.
• Return ONLY the category name (e.g., "Academic"). Do NOT return any explanations, punctuation, or additional text.
------------------------------

POST TITLE: "{text}"
"""

def get_parser():
    parser = argparse.ArgumentParser(description="Classify titles from a tsv file and save into a csv file")
    parser.add_argument("-i", "--input_file", type=str, help="Input tsv file path.")
    parser.add_argument("-o", "--out_file", type=str, required=True, help="Output csv file path.")
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    
    posts = []
    with open(args.input_file, 'r', encoding='utf-8') as infile:
        next(infile)  # Skip header
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                posts.append((parts[0], parts[1]))  # (author_id, title)

    classifications = []
    for post in posts:
        prompt = prompt_template.format(text=post[1])
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        category = response.text.strip()
        classifications.append((post[0], post[1], category))
        time.sleep(4.2)  # To respect rate limits

    with open(args.out_file, 'w', encoding='utf-8') as outfile:
        outfile.write("name,title,coding\n")
        for name, title, category in classifications:
            title = title.replace('"', "'")
            outfile.write(f'"{name}","{title}","{category}"\n')

if __name__ == "__main__":
    main()