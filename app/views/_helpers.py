##############################################
############## HELPER FUNCTIONS ##############
##############################################
###
###     Helper functions are functions that do 
###     not directly render or redirect views but 
###     are used frequently by views.
###

from flask import session
from .. import mongo

            
############## SERVICES ##############        
        
def general_services():
    services = [
        {"title": "Advice", "expert_description": "You surely have tons of insights to offer about your field of expertise, so consider offering advice to those looking for guidance.", "user_description": "Looking for some expert advice? Invite someone specific to offer you some guidance."},
        {"title": "Interview", "expert_description": "Feeling social? Why not charge for your time and allow someone to conduct a quick interview with you?", "user_description": "Looking to dig a little deeper into someone's field of expertise? Consider sending them an interview request."},
        {"title": "Professional Opinion", "expert_description": "Offer some guidance on steps to take for someone unsure about what there next move should be.", "user_description": "Looking for some guidance on how a professional suggests you should approach a certain situation? Consider sending them a request for their professional opinion."},
        {'title': 'Conversation', 'expert_description': 'You have probably gained so much knowledge that many people would find valuable. Why not earn some money by having a simple conversation.', "user_description": "Just want to delve into a topic with someone who has a certain expertise? Send them a conversation request."}, 
        {'title': 'FAQ Email', 'expert_description': 'Up for something more low key? How about charging for a quick Q&A?', "user_description": "Have you got some quick questions that you're looking to have answered? Send a request to someone specific to get some quick answers."}, 
        {'title': 'Lesson', 'expert_description': "Why not play teacher for a bit and bestow some of the knowledge you've gained in your career?", "user_description": "Struggling to understand a complex topic? Send a request to an expert to offer you a tutorial?"}, 
        {"title": "User's Choice", "expert_description": "Some users might have a specific service in mind that you haven't considered, so how about letting them hit you up with an offer?", "user_description": "Have a specific service in mind? Invite an expert to Ambikor and see if they're open to your offer."}
    ]
    return services   

            
############## TEMPLATING ##############        

def career_search_autocomplete():
    careers = []
    for career in mongo.db.careers.find():
        try:
            careers.append({'name': career["title"], 'id': career["career_id"]})
            try:
                for career_title in career["alternative_titles"]:
                    careers.append({'name': career_title, 'id': career["career_id"]})
            except:
                continue
        except:
            mongo.db.careers.delete_one({'_id': career['_id']})
    return [career for career in careers]
        

################## SKELETON TEMPLATES ###################

def get_skeleton():
    user_type = 'admin' if 'admin_username' in session else 'non-user'
    user_type = 'user' if 'user_email' in session else user_type
    template = 'admin/_skeleton_admin.html' if user_type == 'admin' else "_skeleton.html"
    
    login_form = 'none'
    registration_form =  'none'
    
    skeleton = {
        'user_type': user_type,
        'user': mongo.db.users.find_one({"email": session['user_email']}) if 'user_email' in session else 'none',
        'template': "_skeleton_user.html" if user_type == 'user' else template,
        'login_form': login_form,
        'registration_form': registration_form,
        'full_career_list': career_search_autocomplete(),
        'tag_icons': get_tag_icons()
    }
    return skeleton


################## RECOMMENDATIONS ##################

def get_tag_icons():
    icon_cats = ["academic program", "art exhibition", "award", "beauty", "branding", "business", "certificate", "challenge", "coding", "commerce", "community", "competition", "construction", "data", "design", "earth", "education", "experience", "exposure", "fashion", "fellowship", "film festival", "goods", "hackathon", "health", "hospitality", "internship", "job fair", "language", "legal", "math", "media", "music", "networking", "photography", "prize money", "project", "retail", "scholarship", "science", "security", "social good", "space", "sports-rec", "tech", "travel", "trophy", "video", "wildlife", "writing", "xxx"]
    icon_cats_ambits = ["beauty", "branding", "business", "coding", "commerce", "community", "construction", "data", "design", "earth", "education", "fashion", "health", "hospitality", "language", "legal", "math", "media", "music", "photography", "retail", "science", "security", "social good", "space", "sports-rec", "tech", "travel", "video", "wildlife", "writing", "xxx"]
    icons = {"academic program": "../../../static/images/academic_program_icon.png", "art exhibition": "../../../static/images/art_exhibition_icon.png", "award": "../../../static/images/award_icon.png", "beauty": "../../../static/images/cat_beauty.png", "branding": "../../../static/images/cat_goods.png", "business": "../../../static/images/cat_business.png", "certificate": "../../../static/images/certificate_icon.png", "challenge": "../../../static/images/challenge_icon.png", "community": "../../../static/images/cat_community.png", "coding": "../../../static/images/cat_coding.png", "commerce": "../../../static/images/cat_commerce.png", "competition": "../../../static/images/competition_icon.png", "construction": "../../../static/images/cat_structure.png", "data": "../../../static/images/cat_data.png", "design": "../../../static/images/cat_design.png", "earth": "../../../static/images/cat_environment.png", "education": "../../../static/images/cat_education.png", "experience": "../../../static/images/experience_icon.png", "exposure": "../../../static/images/exposure_icon.png", "fashion": "../../../static/images/cat_appearance.png", "fellowship": "../../../static/images/fellowship_icon.png", "film festival": "../../../static/images/film_festival_icon.png", "goods": "../../../static/images/goods_icon.png", "hackathon": "../../../static/images/hackathon_icon.png", "health": "../../../static/images/cat_health.png", "hospitality": "../../../static/images/cat_hospitality.png", "internship": "../../../static/images/internship_icon.png", "job fair": "../../../static/images/job_fair_icon.png", "language": "../../../static/images/cat_language.png", "legal": "../../../static/images/cat_legal.png", "math": "../../../static/images/cat_math.png", "media": "../../../static/images/cat_entertainment.png", "music": "../../../static/images/cat_culture.png", "networking": "../../../static/images/networking_icon.png", "photography": "../../../static/images/cat_photography.png", "prize money": "../../../static/images/prize_money_icon.png", "project": "../../../static/images/project_icon.png", "retail": "../../../static/images/cat_goods.png", "scholarship": "../../../static/images/scholarship_icon.png", "science": "../../../static/images/cat_science.png", "security": "../../../static/images/cat_safeguard.png", "social good": "../../../static/images/cat_social_good.png", "space": "../../../static/images/cat_space.png", "sports-rec": "../../../static/images/cat_recreation.png", "tech": "../../../static/images/cat_electronics.png", "travel": "../../../static/images/cat_travel.png", "trophy": "../../../static/images/trophy_icon.png", "video": "../../../static/images/cat_video.png", "wildlife": "../../../static/images/cat_wildlife.png", "writing": "../../../static/images/cat_writing.png", "xxx": "../../../static/images/cat_xxx.png"}
    return {"icon_cats": icon_cats, "icon_cats_ambits": icon_cats_ambits, "icons": icons}